---
name: system-script-runner
description: 快速调用系统中~/.local/bin下的各类自定义脚本，完成系统更新、清理、软件包管理、媒体处理、虚拟机管理、主题设置、休眠控制等任务。在用户提到系统维护、更新、清理、电池查询、视频转GIF、软件安装卸载、虚拟机管理、护眼模式、Niri blur切换、主题生成、禁用休眠等相关关键词，或直接提到脚本名称时使用。
---

# 系统本地脚本调用技能

## 概述
本技能用于快速响应用户的系统操作需求，自动匹配~/.local/bin下的对应脚本并执行，无需用户记忆复杂命令。

## 可用脚本列表
| 脚本名 | 核心功能 | 触发关键词 | 用法 |
|--------|----------|------------|------|
| checkallupdates | 查看所有待更新软件包，支持交互式更新 | 查更新、待更新、软件更新列表 | 直接运行 `checkallupdates` |
| check-battery | 显示电池健康报告 | 电池、电量、电池健康、电池状态 | 直接运行 `check-battery` |
| clean | 系统垃圾清理（孤儿包、缓存、日志、回收站等） | 清理垃圾、系统清理、清理缓存、删孤儿包 | `clean`（普通清理）/`clean --all`（激进清理） |
| compressvideos | 批量压缩视频文件，支持硬件加速，可提取音频 | 压缩视频、视频压缩、压视频、提取音频、视频转音频 | `compressvideos [选项] <视频文件路径>`，支持 `-q` 指定画质(1-10)、`-d` 指定硬件加速设备、`-o` 提取音频 |
| searchmodels | AI模型浏览器TUI，搜索各大AI提供商可用模型 | 搜模型、找模型、AI模型、模型列表 | 直接运行 `searchmodels`，支持搜索、复制模型名、添加自定义提供商 |
| wifi | 一键连接常用WiFi | 连WiFi、接WiFi、连家里WiFi | 直接运行 `wifi` |
| lsi | 终端预览图片（支持网格浏览） | 预览图片、看图片、终端看图 | `lsi <图片路径/目录路径>` |
| matugen-update | 从壁纸提取颜色生成系统主题色 | 换主题、主题色、生成主题、壁纸取色 | `matugen-update [壁纸路径]` |
| media-info | 显示音视频文件详细信息 | 视频信息、音频信息、媒体信息 | `media-info -f <文件路径>` |
| mirror-update | 自动更新Arch Linux镜像源 | 换源、更新镜像源、镜像源优化 | 直接运行 `mirror-update` |
| niri-blur-toggle | Niri Blur测试版与正式版切换 | 开blur、关blur、切换niri版本、更新niri测试版 | 直接运行 `niri-blur-toggle` |
| niri-sidebar | Niri桌面侧边栏工具 | 打开侧边栏、侧边栏 | 直接运行 `niri-sidebar` |
| nosleep | 禁用系统休眠/挂起 | 禁用休眠、不让电脑休眠、保持唤醒 | 直接运行 `nosleep` |
| pac | Pacman/AUR软件包模糊搜索安装 | 装软件、搜索软件、安装软件 | 直接运行 `pac` |
| pacd | 软件包降级TUI | 降级软件、回退版本 | `pacd [包名]` |
| pacr | 卸载软件TUI（支持Pacman/AUR/Flatpak） | 卸载软件、删软件 | 直接运行 `pacr` |
| pacrrr | 卸载前识别残留配置文件 | 清理残留、删配置文件、彻底卸载 | `pacrrr <软件名/路径>` |
| pak | Flatpak软件包模糊搜索安装 | 装flatpak、flatpak安装 | 直接运行 `pak` |
| preview | 终端预览各种类型文件（图片/视频/文本/压缩包等） | 预览文件、看文件内容 | `preview <文件路径>` |
| pull-upstream | 一键拉取上游仓库最新代码 | 更新脚本、拉取上游、同步配置 | 直接运行 `pull-upstream` |
| searchmodels | 搜索AI模型 | 找模型、搜模型、模型搜索 | `searchmodels <关键词>` |
| sysup | Arch Linux系统更新助手（核心更新脚本） | 更新系统、系统升级、刷系统 | 直接运行 `sysup` |
| toggle-wlsunset | 护眼模式开关（色温调节） | 开护眼、关护眼、护眼模式、色温调节 | 直接运行 `toggle-wlsunset` |
| video2gif | 视频批量转GIF动图 | 转GIF、视频转GIF、动图生成 | `video2gif <视频文件路径>` |
| vir | QEMU/KVM虚拟机管理TUI | 管理虚拟机、开虚拟机、关虚拟机 | 直接运行 `vir` |
| yesleep | 恢复系统休眠/挂起 | 恢复休眠、允许电脑休眠 | 直接运行 `yesleep` |
| wifi | 快捷管理WiFi连接 | 连WiFi、WiFi管理、切WiFi | 直接运行 `wifi` |
| uv | Python极速包管理器 | 装Python包、Python依赖管理 | `uv <子命令>` |
| uvx | 一键运行Python CLI工具 | 运行Python工具、临时执行Python脚本 | `uvx <工具名>` |

## 工作流程
1. 接收用户需求，匹配最适合的对应脚本
2. 确认是否需要参数，需要的话询问用户补充
3. 执行对应脚本，返回执行结果
4. 如果执行出错，给出明确的错误提示和解决建议

## 注意事项
- 涉及系统修改的操作（如sysup、clean、mirror-update等），执行前确认用户权限
- 对于有参数的脚本，确认参数正确后再执行
- 优先使用脚本自带的help信息补充用法说明
- 不要修改脚本本身的内容，除非用户明确要求