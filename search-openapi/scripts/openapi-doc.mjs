#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const DEFAULT_FILE = path.resolve(process.cwd(), 'api.openai.json');
const DEFAULT_LIMIT = 20;
const HTTP_METHODS = new Set(['get', 'post', 'put', 'patch', 'delete', 'head', 'options']);
const ENTITY_PREFIX_RULES = [
  ['/api/subject/company/building/', 'SubjectCompanyBuilding'],
  ['/api/subject/company/', 'SubjectCompany'],
  ['/api/asset/', 'Asset'],
];

function fail(message, code = 1) {
  console.error(message);
  process.exit(code);
}

function printUsage() {
  console.log(JSON.stringify({
    usage: [
      'openapi-doc.mjs show <path-like-query> [--file path] [--method get] [--tag name] [--limit n]',
      'openapi-doc.mjs search <query> [--file path] [--limit n] [--method get] [--tag name]',
    ],
  }, null, 2));
}

function parseArgs(argv) {
  const args = argv.slice(2);
  const command = args.shift();
  if (!command || command === '--help' || command === '-h') {
    printUsage();
    process.exit(0);
  }

  const positionals = [];
  const options = {
    file: DEFAULT_FILE,
    limit: DEFAULT_LIMIT,
    method: '',
    tag: '',
    pretty: false,
  };

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (!arg.startsWith('--')) {
      positionals.push(arg);
      continue;
    }
    if (arg === '--file') {
      options.file = path.resolve(process.cwd(), args[++i] || '');
      continue;
    }
    if (arg === '--limit') {
      const value = Number.parseInt(args[++i] || '', 10);
      if (!Number.isFinite(value) || value <= 0) {
        fail('Invalid --limit, expected positive integer.');
      }
      options.limit = value;
      continue;
    }
    if (arg === '--method') {
      options.method = String(args[++i] || '').toLowerCase();
      if (!HTTP_METHODS.has(options.method)) {
        fail('Invalid --method.');
      }
      continue;
    }
    if (arg === '--tag') {
      options.tag = String(args[++i] || '');
      continue;
    }
    if (arg === '--json') {
      continue;
    }
    if (arg === '--pretty') {
      options.pretty = true;
      continue;
    }
    if (arg === '--compact') {
      options.pretty = false;
      continue;
    }
    fail(`Unknown option: ${arg}`);
  }

  return { command, positionals, options };
}

function readSpec(filePath) {
  if (!fs.existsSync(filePath)) {
    fail(`Spec file not found: ${filePath}`);
  }
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    fail(`Failed to parse spec JSON: ${error.message}`);
  }
}

function normalizeText(value) {
  return String(value || '').toLowerCase();
}

function tokenize(query) {
  return normalizeText(query).split(/\s+/).filter(Boolean);
}

function unique(items) {
  return [...new Set(items.filter(Boolean))];
}

function refName(ref) {
  const parts = String(ref || '').split('/');
  return parts[parts.length - 1] || '';
}

function collectRefs(node, acc = new Set()) {
  if (!node || typeof node !== 'object') {
    return acc;
  }
  if (typeof node.$ref === 'string') {
    acc.add(refName(node.$ref));
  }
  if (Array.isArray(node)) {
    for (const item of node) {
      collectRefs(item, acc);
    }
    return acc;
  }
  for (const value of Object.values(node)) {
    collectRefs(value, acc);
  }
  return acc;
}

function getSchemaMap(spec) {
  return spec.components?.schemas || {};
}

function buildOperations(spec) {
  const operations = [];
  for (const [apiPath, pathItem] of Object.entries(spec.paths || {})) {
    for (const [method, operation] of Object.entries(pathItem || {})) {
      if (!HTTP_METHODS.has(method)) {
        continue;
      }
      const requestSchemaRefs = unique([...collectRefs(operation.requestBody)]);
      const responseSchemaRefs = unique([...collectRefs(operation.responses)]);
      const parameterNames = (operation.parameters || []).map((parameter) => `${parameter.in}:${parameter.name}`);
      const searchFields = [
        apiPath,
        method,
        operation.operationId,
        operation.summary,
        operation.description,
        ...(operation.tags || []),
        ...parameterNames,
        ...requestSchemaRefs,
        ...responseSchemaRefs,
      ];
      operations.push({
        method,
        path: apiPath,
        summary: operation.summary || '',
        description: operation.description || '',
        tags: operation.tags || [],
        operationId: operation.operationId || '',
        parameters: operation.parameters || [],
        requestBody: operation.requestBody || null,
        responses: operation.responses || {},
        requestSchemaRefs,
        responseSchemaRefs,
        searchText: normalizeText(searchFields.join(' ')),
      });
    }
  }
  return operations;
}

function scoreOperation(operation, tokens) {
  let score = 0;
  const loweredPath = normalizeText(operation.path);
  const loweredSummary = normalizeText(operation.summary);
  const loweredDescription = normalizeText(operation.description);
  const loweredOperationId = normalizeText(operation.operationId);
  const loweredTags = operation.tags.map(normalizeText);
  const loweredParams = operation.parameters.map((parameter) => normalizeText(parameter.name));
  const loweredSchemaRefs = [...operation.requestSchemaRefs, ...operation.responseSchemaRefs].map(normalizeText);

  for (const token of tokens) {
    if (loweredPath.includes(token)) {
      score += 50;
    }
    if (loweredPath.split('/').some((segment) => segment.includes(token))) {
      score += 20;
    }
    if (loweredSummary.includes(token)) {
      score += 18;
    }
    if (loweredDescription.includes(token)) {
      score += 12;
    }
    if (loweredOperationId.includes(token)) {
      score += 16;
    }
    if (loweredTags.some((tag) => tag.includes(token))) {
      score += 14;
    }
    if (loweredSchemaRefs.some((name) => name.includes(token))) {
      score += 10;
    }
    if (loweredParams.some((name) => name.includes(token))) {
      score += 6;
    }
    if (operation.searchText.includes(token)) {
      score += 2;
    }
  }

  return score;
}

function resolveSchemaClosure(schemaMap, refs) {
  const resolved = {};
  const queue = [...refs];
  const seen = new Set(queue);

  while (queue.length > 0) {
    const name = queue.shift();
    const schema = schemaMap[name];
    if (!schema) {
      continue;
    }
    resolved[name] = schema;
    for (const childRef of collectRefs(schema)) {
      if (!seen.has(childRef)) {
        seen.add(childRef);
        queue.push(childRef);
      }
    }
  }

  return resolved;
}

function inferEntity(operation) {
  const nonResponseRefs = unique(
    [...operation.responseSchemaRefs, ...operation.requestSchemaRefs].filter((name) => !name.startsWith('ResponseBo')),
  );
  if (nonResponseRefs.length === 1) {
    return nonResponseRefs[0];
  }
  for (const [prefix, entity] of ENTITY_PREFIX_RULES) {
    if (operation.path.startsWith(prefix)) {
      return entity;
    }
  }
  return 'unknown';
}

function groupParameters(parameters) {
  const grouped = {};
  for (const parameter of parameters) {
    const group = parameter.in || 'unknown';
    if (!grouped[group]) {
      grouped[group] = [];
    }
    grouped[group].push({
      name: parameter.name,
      required: Boolean(parameter.required),
      description: parameter.description || '',
      schema: parameter.schema || null,
      example: parameter.example ?? parameter.schema?.example ?? null,
    });
  }
  return grouped;
}

function toDetail(spec, operation) {
  const schemaMap = getSchemaMap(spec);
  const schemaRefs = unique([...operation.requestSchemaRefs, ...operation.responseSchemaRefs]);
  return {
    method: operation.method,
    path: operation.path,
    summary: operation.summary,
    description: operation.description,
    tags: operation.tags,
    operationId: operation.operationId,
    parameters: groupParameters(operation.parameters),
    requestBody: operation.requestBody,
    responses: operation.responses,
    requestSchemaRefs: operation.requestSchemaRefs,
    responseSchemaRefs: operation.responseSchemaRefs,
    schemaRefs,
    inferredEntity: inferEntity(operation),
    schemas: resolveSchemaClosure(schemaMap, schemaRefs),
  };
}

function filterOperations(operations, options) {
  return operations
    .filter((operation) => !options.method || operation.method === options.method)
    .filter((operation) => !options.tag || operation.tags.includes(options.tag));
}

function sortPrefixMatches(matches) {
  return [...matches].sort((left, right) => left.path.localeCompare(right.path) || left.method.localeCompare(right.method));
}

function sortFuzzyMatches(matches, tokens) {
  return matches
    .map((operation) => ({ operation, score: scoreOperation(operation, tokens) }))
    .filter((item) => item.score > 0)
    .sort((left, right) => right.score - left.score || left.operation.path.localeCompare(right.operation.path) || left.operation.method.localeCompare(right.operation.method));
}

function findOperation(operations, identifier, method) {
  let matches;
  if (identifier.startsWith('/')) {
    matches = operations.filter((operation) => operation.path === identifier);
  } else {
    matches = operations.filter((operation) => operation.operationId === identifier);
  }
  if (method) {
    matches = matches.filter((operation) => operation.method === method);
  }
  if (matches.length === 0) {
    return null;
  }
  if (matches.length > 1) {
    fail(`Multiple operations matched ${identifier}; rerun with --method.`);
  }
  return matches[0];
}

function showOperations(spec, operations, query, options) {
  if (!query) {
    fail('show requires a path-like query or operationId.');
  }

  const filtered = filterOperations(operations, options);
  const exact = findOperation(filtered, query, options.method);
  if (exact) {
    return toDetail(spec, exact);
  }

  if (query.startsWith('/')) {
    const prefixMatches = sortPrefixMatches(filtered.filter((operation) => operation.path.startsWith(query))).slice(0, options.limit);
    if (prefixMatches.length > 0) {
      return prefixMatches.map((operation) => toDetail(spec, operation));
    }
    fail(`Operation not found: ${query}`);
  }

  const tokens = tokenize(query);
  if (tokens.length === 0) {
    fail('show requires a non-empty query.');
  }
  const fuzzyMatches = sortFuzzyMatches(filtered, tokens).slice(0, options.limit).map((item) => toDetail(spec, item.operation));
  if (fuzzyMatches.length === 0) {
    fail(`Operation not found: ${query}`);
  }
  return fuzzyMatches;
}

function searchOperations(operations, query, options) {
  const tokens = tokenize(query);
  if (tokens.length === 0) {
    fail('search requires a non-empty query.');
  }

  return sortFuzzyMatches(filterOperations(operations, options), tokens)
    .slice(0, options.limit)
    .map(({ operation, score }) => ({
      score,
      method: operation.method,
      path: operation.path,
      summary: operation.summary,
      description: operation.description,
      tags: operation.tags,
      operationId: operation.operationId,
      requestSchemaRefs: operation.requestSchemaRefs,
      responseSchemaRefs: operation.responseSchemaRefs,
    }));
}

function writeJson(value, pretty) {
  process.stdout.write(`${JSON.stringify(value, null, pretty ? 2 : 0)}\n`);
}

function main() {
  const { command, positionals, options } = parseArgs(process.argv);
  const spec = readSpec(options.file);
  const operations = buildOperations(spec);

  if (command === 'show') {
    writeJson(showOperations(spec, operations, positionals[0], options), options.pretty);
    return;
  }

  if (command === 'search') {
    writeJson(searchOperations(operations, positionals.join(' '), options), options.pretty);
    return;
  }

  fail(`Unknown command: ${command}`);
}

main();
