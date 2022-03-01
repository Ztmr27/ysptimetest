# YSPTimeConsuming

![stream](https://stream.woa.com/pipeline/stream/api/external/stream/projects/838828/pipelines/badge?file_path=.ci/codecc.yml&branch=master)

## 概述
* 央视频双端耗时类测试全自动化实践
* 核心方法：
    * 通过Ui自动化 + 录屏工具实现自动录屏
    * 通过`stagesepx`自动分析录屏视频，计算耗时
    * 关于`stagesepx`请参考：[基于stagesepx的启动耗时测试](http://km.oa.com/articles/show/449252)

## 环境依赖
* Python 3.6+ (pip依赖见：`requirements.txt`)
* iOS端Ui自动化工具：[facebook-wda](https://github.com/openatx/facebook-wda)
* iOS端录屏工具：[xrecord](https://github.com/WPO-Foundation/xrecord)（已导入到脚本）
* 安卓Ui自动化工具：[uiautomator2](https://github.com/openatx/uiautomator2)
* 安卓端录屏工具：[scrcpy](https://github.com/Genymobile/scrcpy)
* 视频自动拆帧&分析：[stagesepx](https://github.com/williamfzc/stagesepx)


## 框架结构
* main.py - 主脚本
* workflow.py - 业务工作流
    * 主要包括：`Capture` 和 `Analyze`
* capture - 录屏模块
* analyze - 视频分析模块
* public - 公共类模块
* shell - shell脚本
* model - 训练模型
* tools - 第三方工具
* config/config.ini - 配置文件
* output/ - 输出内容

## 使用说明
* 安卓/iOS测试机连接电脑（最好保证每一你端设备只连接一个）
    * 安卓打开开发者模式，iOS信任手机
    * 双端可同时连接测试，支持并行运行
* 在配置文件`config.ini` - `Main`中配置参数，`python3 main.py`
* 或`python3 main.py` + 运行参数，详情如下：
```bash
(venv) ➜  YSPTimeConsuming git:(master) ✗ python3 main.py -h                        
Using TensorFlow backend.
usage: main.py [-h] [-p PLATFORM] [-t TYPE] [-n NAME] [-r ROUNDS] [-nth]
               [-nrp] [-ntx]

specify running mode

optional arguments:
  -h, --help            show this help message and exit
  -p PLATFORM, --platform PLATFORM
                        the platform to be run
  -t TYPE, --type TYPE  case_type, according to the `case_type` to run the
                        specified case set
  -n NAME, --name NAME  case_name, according to the `case_name` to run the
                        specified case
  -r ROUNDS, --rounds ROUNDS
                        rounds, according to the `rounds` specify repeat times
  -nth, --thread        thread, according to the `thread` specify whether use
                        thread when two platform input
  -nrp, --report        report, whether output a report or not, True default
  -ntx, --txt           txt, whether output result to text or not, True
                        default
```

## 配置文件说明
* platform - 待运行的平台，android/ios（也可以简写：a/i）
* case_type - case类型：app/tv/video，为空表示全部类型
* case_name - 具体case名，为空表示全部case
* rounds - 每条case重复的次数
* 目前只支持3种运行组合：
    * 全部case
    * 某一个case_type下的所有case
    * 某一个具体case，即通过case_type 和 case_name组合指定
```ini
# --- Main Config --- #
[Main]
platform = iOS,Android
case_type =
case_name =
rounds = 5
```

## 开发规范
1. 分支开发，通过工蜂发起mr和cr，合入主干时务必通过 [通用代码质量红线](https://git.woa.com/ci_templates/public/codecc/blob/master/.ci/templates/commonGate.yml)
2. 代码规范需符合 [腾讯代码规范](https://git.woa.com/standards/python)
3. 每次提交代码会自动触发codecc代码扫描（按照：公司内部开源治理要求进行扫描），请及时处理代码缺陷
4. 代码提交符合[约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/)

    
    
    
    
    
    