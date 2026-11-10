# CLI 发布流程

2026-10-23 使用 CloudBase CLI 3.8.8 实测：从独立的预构建目录执行 `tcb app deploy`，能更新已有静态应用、生成新版本记录并发布至原子路径。以下是命令模板；替换目标变量，执行前查当前版本帮助，不把本次版本号或耗时当作平台保证。

## 登录与定位

```sh
tcb -v
tcb env list --json
```

已登录且可读取目标环境时继续，不重复登录。未安装时使用 `npm install -g @cloudbase/cli`；认证失效时先看 `tcb login --help`，按用户选择使用 `tcb login` 浏览器授权或 `tcb login --key` 交互输入凭据。不要将账户凭据写入本技能、项目配置或发布物。

结合项目已有发布记录与只读查询确认环境、地域、应用/服务、挂载路径和旧版本。环境唯一不等于应用唯一；不能仅凭环境列表就创建或覆盖服务。

## 静态网站：发布应用新版本

需要应用版本管理时使用 `app deploy`；`hosting deploy` 仅上传文件，即使页面更新也不代表新增应用版本。先核对：

```sh
tcb app deploy --help
tcb app info "$SERVICE" -e "$ENV_ID" --json
tcb app versions list "$SERVICE" -e "$ENV_ID" --json
```

`SERVICE`、`ENV_ID`、`DEPLOY_PATH`、`RELEASE_DIR` 分别是已确认的应用名、环境 ID、云端挂载路径和独立发布目录的绝对路径。优先复用已有应用和路径。共享根站点下更新子应用时，发布前记录根入口内容指纹。

按项目脚本构建并运行相关测试。独立目录应包含完整产物，上传期间保持内容稳定；不要直接使用正被开发服务或其他构建改写的 `dist/`。发现产物改变时先停止该次上传，重新准备稳定目录并核查线上入口，再有范围地重试。

子路径项目同时配置构建资源前缀和平台挂载路径；`--deploy-path` 不会重写已经构建的 HTML/JS。按项目技术栈设置构建前缀，不能假设某个环境变量对所有项目通用。例如支持 `DEPLOY_BASE_PATH` 的 Vite 项目可这样构建：

```sh
DEPLOY_BASE_PATH="$DEPLOY_PATH/" npm run build -- --outDir "$RELEASE_DIR"
```

该例假设 `DEPLOY_PATH` 是不含结尾斜杠的子路径；根路径构建按项目规则使用 `/`。检查入口 HTML 的资源引用及运行时数据、Worker 路径。检查文件清单，排除源环境文件、依赖目录及其他非发布资料。

对已经构建好的产物，跳过云端安装与构建：

```sh
tcb app deploy "$SERVICE" -e "$ENV_ID" \
  --cwd "$RELEASE_DIR" \
  --framework static \
  --install-command '' \
  --build-command '' \
  --output-dir ./ \
  --deploy-path "$DEPLOY_PATH"
```

看到覆盖提示，核对它指向已授权的目标应用后确认。不要通过改名创建重复应用来回避覆盖确认。CLI 可能在工作目录保存 `cloudbaserc.json`；检查它的位置和内容，避免误写其他项目配置，或把部署后生成的配置误计为已上传产物。

记录 CLI 返回的版本名、任务/BuildId、访问 URL 与耗时。查对应版本：

```sh
tcb app info "$SERVICE" -e "$ENV_ID" --json
tcb app versions detail "$SERVICE" --version-name "$VERSION" -e "$ENV_ID" --json
```

静态托管的 `TrafficPercent: 0` 或空 `CurrentVersion` 字段不能直接按容器流量语义解释。结合 `SUCCESS`、最新版本名及线上内容判断是否生效。CLI 返回的应用域名与已有环境子路径 URL 可能不同，应实际验证交付链接，不只复制命令输出。

## 云托管：代码或镜像部署

```sh
tcb cloudrun deploy --help
tcb cloudrun list --help
tcb cloudrun list -e "$ENV_ID"
```

确认当前环境适用的命令代际、服务类型和已有配置。容器代码部署示例：

```sh
tcb cloudrun deploy -e "$ENV_ID" -s "$SERVICE" \
  --source "$SOURCE_DIR" --port "$PORT"
```

已有镜像可按当前帮助使用 `--imageUrl`。端口仅适用于容器型服务；本地容器验证用 Docker，不能用仅支持函数型服务的 `tcb cloudrun run` 代替。

发布前查明是否自动接管流量，按约定决定灰度或完整替换。`--traffic`、`--wait`、版本与流量子命令以已安装版本帮助为准，不复制其他版本的参数或假设它们可以同时使用。分别核对任务、服务健康、实际流量及公网结果；不能仅以命令退出成功宣布完成。

## 验收与停止条件

按 [verification.md](verification.md) 验证最终 URL 与核心业务路径。静态项目比较线上入口、JS/CSS、代表性数据和必要静态资源与独立发布物的内容指纹，检查原站点入口未被覆盖，并在浏览器实际打开页面。测试域名中间页应正常点击继续，不伪造请求头绕过。

认证、权限、环境状态或额度问题无法在授权范围解决时，报告具体错误及需要用户完成的动作。上传或任务等待使用有界观察，先查状态和日志，再决定是否重试；不要因等待无输出重复提交。部署和验收完成即停止。

官方入口：[应用管理](https://docs.cloudbase.net/cli-v1/app/management)、[云托管部署](https://docs.cloudbase.net/cli-v1/cloudrun/deploy)。
