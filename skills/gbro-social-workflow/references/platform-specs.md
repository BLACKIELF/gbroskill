# 平台规格、封面和话题

制作和发布前按本页核对具体入口、账号、内容类型和当前界面。平台限制会变；官方 API、网页、手机 App、会员账号不能互相套用。下表明确区分「当前账号网页实测」「官方接口说明」「GBro 制作建议」；未获一手证据的项目不编硬上限。核验时间、账号和原文保存在本次作品或运行根 QA 中。

## 封面制作

以下像素是 GBro 制作建议；与平台确认的比例分开标注。尺寸适配优先保持关键画面和标题，不把一张封面机械拉伸到所有渠道。封面先导出清晰 JPG/PNG，一般控制在 2MB 内；这是一项制作预算，不是各平台统一硬上限。

| 平台／内容 | 制作尺寸与比例 | 注意事项 |
|---|---|---|
| 小红书图文 | 1080×1440，3:4 | 封面计入AiGoodBro 品牌预设单条最多 9 张图的交付约定；不把 9 张冒称平台实时上限 |
| 小红书视频封面 | **1600×1200，4:3** | 沿用AiGoodBro 品牌预设已确认的样稿；如当轮明确改比例则按当前要求，上传后检查裁切 |
| 微博视频 | 横向 1600×1200（4:3）或 1920×1080（16:9）；竖向 1080×1440（3:4） | [官方](https://kefu.weibo.com/faqdetail?id=21503)支持这些封面比例；竖视频不用横封面。本机 SAU 要求提供封面，校验预算严格小于 5MiB |
| 抖音 | 同时准备竖封面 1080×1440（3:4）与横封面 1920×1080（16:9） | 属于制作建议及本机工具支持的双封面；按当前编辑器裁切区分别确认 |
| TikTok | 沿用成片画幅；竖版展示预览可另做 1080×1920（9:16） | 属于制作建议；本机 autotok 尚无已核实的独立封面上传能力，须在实际入口核可选帧与展示裁切，不把准备了封面写成已设置成功 |
| B站 | 1920×1080，16:9；重要字与主体在中央，另检查 4:3 展示裁切 | 属于制作建议；历史官方 1146×717 不能当成当前唯一强制尺寸。确认实际投稿封面比例与文件限制 |
| 视频号 | 按实际横／竖编辑器制作，建议横 1920×1080、竖 1080×1440；出现 6:7 封面入口时另做 1080×1260 | 不把视频比例、封面裁切和列表展示比例混为一项；以当前编辑器框线核验 |
| X | 图文横卡 1600×900（16:9），视频封面跟随成片画幅 | 属于制作建议；标题不贴边，手机与网页均检查展示。视频原画幅优先保留 |
| YouTube／Metricool | 普通视频缩略图 1280×720（16:9）；Shorts 1080×1920（9:16） | [Metricool 指南](https://help.metricool.com/schedule-and-publish-on-youtube-gof0k)给出以上规格；Shorts 自定义封面依频道验证与功能开放情况。YouTube [官方缩略图规则](https://support.google.com/youtube/answer/72431?hl=en)区分手机视频缩略图 2MB 与桌面 50MB；不把它们冒称 Metricool 的上传上限，连接器文件限制另核 |
| 公众号普通图文 news | 主封面 1410×600（2.35:1）及方形 1080×1080（1:1） | 当前[草稿接口](https://developers.weixin.qq.com/doc/subscription/api/draftbox/draftmanage/api_draft_add.html)的 news 裁剪支持 2.35:1 与 1:1；两种裁切分别检查标题与头像 |
| 公众号图片消息 newspic | 按当前消息形态选择 1:1、16:9、2.35:1 | 来自同一草稿接口；不把 newspic 比例当普通 news 的通用比例 |
| 小程序会话分享图 | 1000×800，5:4 | 5:4 限定为 [onShareAppMessage](https://developers.weixin.qq.com/miniprogram/dev/reference/api/Page.html) 的 imageUrl 显示；朋友圈分享与页面海报另查对应接口 |

AiGoodBro 品牌预设新制作视频默认 4:3、至少 1440×1080；原片保持原画幅。平台封面建议不改变成片默认，不为适配封面裁掉视频里的字幕、操作界面或人物。

## 上传大小、格式和时长

| 入口 | 已核实的限制／状态 | 执行方式 |
|---|---|---|
| 抖音当前账号创作中心网页 | 上传页面写明 **1 小时以内、16G 以内**；支持 4K；建议画幅 16:9、9:16、3:4、4:3、9:19.5 | 当前账号实测；推荐 MP4/H.264。页面另建议超过 40 秒用横版，不将建议冒称强制规则 |
| 抖音开放 API upload-video | [官方文档](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/video-management/douyin/create-video/upload-video)：总文件不超过 4GB；大于 50MB 建议分片，大于 300MB 必须分片 | 单独列为 API 入口，需对应权限；不能据此把网页限制写成 4GB |
| TikTok Content Posting API | [官方媒体指南](https://developers.tiktok.com/docs/en/content-posting-api-media-transfer-guide)：视频最多 4GB，MP4/WebM/MOV，H.264/H.265/VP8/VP9，23—60fps，宽高各 360—4096；上传初始化最长 10 分钟，最终可发时长依账号权限 | 属于官方 API 限制，不能直接套本机 autotok 或网页入口；本机工具的大小／时长上限和账号能力仍需发布前核验。推荐 MP4/H.264/AAC，不把测试连通当发布验证 |
| 小红书当前账号网页视频 | 上传页写明 **4 小时以内、最大 20GB**；常用格式，推荐 MP4/MOV；超过 1080P 建议网页上传 | 当前账号实测；前端文件校验另为 `<20×2^30 bytes`，靠近边界时按实际校验结果处理。不可沿用旧的 4GB／15 分钟通用说法 |
| 小红书图文 | 图片文件大小、当前可选张数及单图格式在图文上传入口实时读取 | AiGoodBro 品牌预设 9 图约定不等于平台上限；建议 JPG/PNG，单图 2MB 内。未核到当前硬上限时明确记录待核，不猜 20MB／50 张 |
| B站当前账号网页视频 | 上传页写明 **16G 以内、10 小时以内**；**粉丝数 ≥1000 可自动解锁 64G**；推荐 MP4/MOV/MKV、1080P/4K | 当前账号实测；不得假定本账号已解锁 64G。biliup 使用的实际投稿线路另做同稿前置检查，不能把网页提示当所有线路保证 |
| 视频号网页 | 当前登录有效；上传容量和时长需在本账号实际投稿界面读取 | 历史 2GB／1 小时不能冒称当前统一上限。未核明前用 MP4/H.264，制作预算小于 2GB、短于 1 小时，并标注预算与待核边界；超预算不是直接宣布平台不支持 |
| 微博网页视频 | [官方客服](https://kefu.weibo.com/faqdetail?id=21503)：**电脑 15G、手机 4G**；手机端至少 3 秒 | 标题至少 6 字；本机 SAU 标题最多 30 字属工具限制。2K/4K 播放权限及转码状态按实际账号和页面核对，不把源文件分辨率当已公开清晰度 |
| X 普通账号网页 | [官方](https://help.x.com/en/using-x/x-videos)：**140 秒、512MB** | 按账号真实权限执行；推荐 MP4/H.264/AAC，并等处理完成再提交 |
| X Premium 网页 | 官方最长 **不足 4 小时、16GB**；长视频分辨率条件另有限制 | 2 小时以内优先 1080P，2—4 小时优先 720P；官方说明与账号界面有变化时重新核查。不能套旧版脚本的 60 分钟，也不自动购买会员 |
| X 图片 | 本机脚本最多处理 4 张；网页当前格式、单图大小另核 | 4 张首先记作已安装工具行为；GBro 建议 JPG/PNG、单图小于 5MB，不冒称对所有入口的官方硬上限 |
| YouTube 经 Metricool | [Metricool 官方](https://help.metricool.com/schedule-and-publish-on-youtube-gof0k)：MP4/MOV、最大 500MB；标题最多 100 字符，描述工具预算 5000 字符；普通视频／Shorts 按当前入口分类 | 500MB 属于 Metricool 通道限制。未验证频道的 15 分钟限制、受众选择、可见性和声明逐项检查；保持清晰主文件，需要压缩时另存传输版 |
| YouTube 原生上传 | [YouTube 官方](https://support.google.com/youtube/answer/71673?hl=en)：最大 256GB 或 12 小时，以先达到者为准；默认最多 15 分钟，验证账号可发更长视频 | 不能用此上限替代 Metricool 的 500MB；频道当前权限和实际上传入口仍需核对 |
| 公众号永久素材 API | [官方](https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_addmaterial.html)：image 10M，bmp/png/jpeg/jpg/gif；video 10MB、MP4；专门的 thumb 类型 64KB、JPG | 封面 thumb_media_id 是素材 ID 字段，不能把 thumb 类型 64KB 限制套到所有封面；按实际上传素材类型处理。公众号后台网页视频上限与此接口分开核查 |
| 公众号正文图片 API uploadimg | [官方](https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_uploadimage.html)：JPG/PNG、1MB 以下 | 正文图先压缩到接口预算再上传；不能用该接口上限代替永久 image 素材限制 |
| 小程序 | 无通用“视频发帖最大大小” | 按本项目实际云存储、页面、分享接口和已接入官方通道核对；不新增平台能力或自动发版 |

发布规格保留原工作流核验日期与入口差异，但私人账号网页快照不随包提供。目标账号临近上限时须重新核对编辑器；不能把历史入口快照当成普遍官方保证。

## 各平台 tag／话题

凡本次入口支持话题或标签，按AiGoodBro 品牌预设长期要求固定带 `AiGoodBro`，计入总数；其他词先服务本篇内容和读者检索，再考虑真实且相关的活动。下表区分用户指定数量、GBro 编辑预算、官方推荐和入口硬上限；不同入口不能互套。未核实的硬上限明确标注待核，不默认塞 `#上热门`，不承诺流量。

### AI 短剧类固定话题

发布 AI 短剧成片，或分享这类作品的提示词、制作教程时，所有实际支持话题／标签的入口固定带以下四项，计入去重后的总数：

```text
#AiGoodBro #AI短剧 #AI视频制作 #提示词分享
```

小红书仍为 10 个不重复话题，由这 4 个固定项加 6 个本篇贴题话题组成。其他平台保留四个固定项，再按内容添加必要话题；本类稿的固定项优先于下表较少的编辑预算，包括视频号的通用 1—3 个建议。各项按平台写法选择实际话题／标签；若实际入口硬上限不足 4 个，停在提交前说明冲突，不擅自省略固定项。没有话题／标签功能的入口不硬加。这组固定项只用于 AI 短剧及其相关提示词、教程发布，不套用到无关稿件。

### 各平台写法与数量

| 平台 | 写法／位置 | 本包默认预算与核验 |
|---|---|---|
| X | `#AiGoodBro` 加相关 `#关键词`；词内不含空格和标点 | 总计 1—2 个；[官方说明](https://help.x.com/en/using-x/how-to-use-hashtags)建议不超过 2 个，但明确允许更多，2 不是硬上限；仍受正文长度限制 |
| 微博 | 必带 `#AiGoodBro#`，再选本篇核心 `#话题名称#`；有闭合井号 | 默认总计 2 个，按[官方客服推荐](https://kefu.weibo.com/faqdetail?id=21594)；这是贡献度／阅读量规则，不是编辑器只能输入 2 个。[话题官方说明](https://www.sina.cn/news/detail/5285472228346322.html)称每篇 ≥3 个无法积累贡献度；技术硬上限待本入口实测。超级话题单独处理 |
| 抖音 | 描述区输入并选择实际候选，必带 `#AiGoodBro` | 暂按总计 3—5 个的制作预算；[普通创建视频 API](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/video-management/douyin/create-video/video-create)未给话题个数上限，普通创作入口硬上限待核。[小程序“拍抖音任务”API](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/server/basic-abilities/share/douyin_task/create-task)的 tags 最多 10 个仅适用该专项接口 |
| 小红书 | 正文通过候选选择话题，必带 `#AiGoodBro` | **总计 10 个不重复话题**：1 个品牌 + 9 个贴题话题。[官方发布页代码](https://fe-static.xhscdn.com/formula-static/ugc/public/resource/js/project-publish-vue.474cd180.js)有 10 个校验及对应提示；另有受限模式 3 个分支，若实际页面提示更少，保留品牌话题并停在提交前报告，不能强行绕过或静默减数。候选失败不得静默跳过；不要手写内部 `[话题]#` 标记 |
| TikTok | caption 中必带 `#AiGoodBro`，其余按内容及目标受众选词 | 暂按总计不超过 5 个的保守预算；[Planoly 的 App 观察](https://www.planoly.com/blog/tiktok-5-hashtag-limit)报告 5 个限制，属第三方观察，本账号网页／所选上传工具的硬上限待实测，不与官方 API 的正文长度混为一项 |
| YouTube | 描述中必带 `#AiGoodBro`；后台 tags 字段与正文 hashtag 分别处理，使用 tags 时也包含 `AiGoodBro` | GBro 通用预算 3—5 个相关 hashtag，AI 短剧类保留四个固定项；[官方规则](https://support.google.com/youtube/answer/6390658?hl=en)规定超过 60 个会忽略全部 hashtag，标题附近最多显示 3 个，不等于最多只能加 3 个。[API tags](https://developers.google.com/youtube/v3/docs/videos)总长最多 500 字符，分隔逗号及含空格项的引号计入；不能与 hashtag 个数混算 |
| B站 | 投稿后台“标签”字段必填 `AiGoodBro`；工具用逗号分隔 | 暂按总计 3—8 个的制作预算，常见 10 个上限仍需当前官方编辑器确认；不把 `#...#` 粘进标签字段。话题活动另设，不与投稿标签混算 |
| 视频号 | 视频描述内选话题，必带 `#AiGoodBro` | 总计 1—3 个是制作预算，硬上限待当前编辑器确认；活动、位置、声明分别处理，不照搬全部小红书话题 |
| 公众号 | **当前官方 [draft/add](https://developers.weixin.qq.com/doc/subscription/api/draftbox/draftmanage/api_draft_add.html) 没有文章 tags 字段，默认不追加社交话题尾巴** | [用户标签接口](https://developers.weixin.qq.com/doc/subscription/api/usermanage/tag/api_createtag.html)用于用户分组，不是文章话题。后台若实际提供话题、合集／系列，分别读取并按本次授权设置；实际支持话题时同样带 `AiGoodBro`，不能将合集等同于话题或声称所有公众号界面都“没有 tag” |
| 小程序 | [分享接口](https://developers.weixin.qq.com/miniprogram/dev/reference/api/Page.html)无通用社交发帖 tag | 仅沿用项目已经存在且本次适用的搜索词／分类字段；只有真实话题／标签功能才应用品牌规则，不自行发明字段或追加功能 |

全平台只要本次入口能带话题／标签，就固定带 `AiGoodBro`，品牌项计入总数；没有该功能的入口不追加品牌署名或杜撰分类字段。平台稿分别保存标题、正文、话题和适用评论。发布前逐个核对必带词、去重后数量及可点击话题／实际标签；主题不匹配的热词不选。公众号与小程序不会自动继承其他渠道 hashtag。

## 发布前最小检查

- 用 ffprobe 或现有媒体工具读实际编码、时长、宽高和文件字节数；文件扩展名不能替代格式验证。中文硬字幕需实际播放并抽看首、中、尾，检查遮挡、截断和同步。
- 对照本入口限制检查主视频、封面、正文图；保留高清主文件，需要压缩时另存传输版并记录实际规格。当前账号未具备高清或长视频权限时不虚报。
- 标题不静默截断；超长先改稿并回读。配图、封面、正文与视频表达一致，陌生缩写在首图或第二图解释。
- 支持话题／标签的入口必须出现准确的 `AiGoodBro`；AI 短剧类还要逐项核对上方四个固定话题。核对平台写法、去重后总数以及最终可点击话题／实际标签。小红书总计 10 个；其他渠道按本类固定项、上表和当前入口校验。不以正文里提到品牌代替真正的话题或标签。
- 内容声明、自制／转载、来源署名和平台必填字段按作品事实填写；不绕过平台自动标注或强制声明，也不无依据地自动替用户勾选。
- 上传、审核、公开和去重按[工具规则](platform-tools.md#提交与回读)执行；通过规格检查不等于已发布。
