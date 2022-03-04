# -*- coding: utf-8 -*-
"""
@Author: Ssfanli
@Time  : 2021/01/14 3:56 下午
@Desc  : 
"""

# html主干: style=STYLE_TMPL, tables
HTML_TMPL = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>PerfReport</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
%(style)s
</head>
<body>
    <script language="javascript" type="text/javascript">
        function show_img(obj) {
            var obj1 = obj.nextElementSibling
            obj1.style.display='block'
            var index = 0;//每张图片的下标，
            var len = obj1.getElementsByTagName('img').length;
            var imgyuan = obj1.getElementsByClassName('imgyuan')[0]
            //var start=setInterval(autoPlay,500);
            obj1.onmouseover=function(){//当鼠标光标停在图片上，则停止轮播
                clearInterval(start);
            }
            obj1.onmouseout=function(){//当鼠标光标停在图片上，则开始轮播
                start=setInterval(autoPlay,1000);
            }
            for (var i = 0; i < len; i++) {
                var font = document.createElement('font')
                imgyuan.appendChild(font)
            }
            var lis = obj1.getElementsByTagName('font');//得到所有圆圈
            changeImg(0)
            var funny = function (i) {
                lis[i].onmouseover = function () {
                    index=i
                    changeImg(i)
                }
            }
            for (var i = 0; i < lis.length; i++) {
                funny(i);
            }

            function autoPlay(){
                if(index>len-1){
                    index=0;
                    clearInterval(start); //运行一轮后停止
                }
                changeImg(index++);
            }
            imgyuan.style.width= 25*len +"px";
            //对应圆圈和图片同步
            function changeImg(index) {
                var list = obj1.getElementsByTagName('img');
                var list1 = obj1.getElementsByTagName('font');
                for (i = 0; i < list.length; i++) {
                    list[i].style.display = 'none';
                    list1[i].style.backgroundColor = 'white';
                }
                list[index].style.display = 'block';
                list1[index].style.backgroundColor = 'red';
            }
        }

        function hide_img(obj){
            obj.parentElement.style.display = "none";
            obj.parentElement.getElementsByClassName('imgyuan')[0].innerHTML = "";
        }
    </script>
    <h1> 性能数据对比报告 </h1>
    %(tables)s
    %(additional_desc)s
</body>
</html>
"""

# style单独拎出来，避免和格式化冲突 ⚠️ ⚠️ ⚠️
STYLE_TMPL = """
<style type="text/css">
html {
    font-family: sans-serif;
    -ms-text-size-adjust: 100%;
    -webkit-text-size-adjust: 100%;
}

body {
    margin: 10px;
}
table {
    border-collapse: collapse;
    border-spacing: 0;
}

td,th {
    height: 15px;
    line-height: 20px;
    padding: 0;
}

.footer {
        position: relative;
        height: 40px;
        bottom: 20px;
        left: 0px;
        right: 0px;
        text-align: center;
    }
.pure-table {
    border-collapse: collapse;
    border-spacing: 0;
    empty-cells: show;
    border: 1px solid #cbcbcb;
}

.pure-table caption {
    color: #000;
    font: italic 85%/1 arial,sans-serif;
    padding: 1em 0;
    text-align: center;
}

.pure-table td,.pure-table th {
    border-left: 1px solid #cbcbcb;
    border-width: 0 0 0 1px;
    font-size: inherit;
    margin: 0;
    overflow: visible;
    padding: .5em 1em;
}

.pure-table thead {
    background-color: #e0e0e0;
    color: #000;
    text-align: left;
    vertical-align: bottom;
}

.pure-table td {
    background-color: transparent;
}

.pure-table-bordered td {
    border-bottom: 1px solid #cbcbcb;
}

.pure-table-bordered tbody>tr:last-child>td {
    border-bottom-width: 0;
}

/* -- screenshots ---------------------------------------------------------------------- */
.img {
    height: 100%;
    border-collapse: collapse;
}
.screenshots {
    z-index: 100;
    position: fixed;
    height: 80%;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
    display: none;
    box-shadow: 1px 2px 20px #333333;
}

.imgyuan {
    height: 20px;
    border-radius: 12px;
    background-color: red;
    padding-left: 13px;
    margin: 0 auto;
    position: relative;
    top: -40px;
    background-color: rgba(1, 150, 0, 0.3);
}
.imgyuan font{
    border:1px solid white;
    width:11px; 
    height:11px;
    border-radius:50%;
    margin-right: 9px;
    margin-top: 4px;
    display: block;
    float: left;
    background-color: white;
}

.close_shots {
    background-image: url(data:image/png;base64,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);
    background-size: 22px 22px;
    -moz-background-size: 22px 22px;
    background-repeat: no-repeat;
    position: absolute;
    top: 5px;
    right: 5px;
    height: 22px;
    z-index: 99;
    width: 22px;
    ox-shadow:1px 2px 5px #333333;
}
</style>
"""

# 补充说明和结尾
ADDITIONAL_DESC = """
    <h3>
        三、补充说明
    </h3>
    <b><span style="line-height:2;">1. 真实启动耗时：</span><span style="line-height:2;">：</span></b><span style="line-height:2;">等于程序启动耗时 + 广告加载耗时</span><br />
    <b><span style="line-height:2;">2. 程序启动耗时：</span></b><span style="line-height:2;">对应启动数据上报的launch_time</span><br />
    <b><span style="line-height:2;">3. 广告加载耗时：</span></b><span style="line-height:2;">对应启动数据上报的ad_load_time</span><br />
    
    <h3>
        附录
    </h3>
    1. <a href="https://doc.weixin.qq.com/sheet/e3_AHoAEAbcACk9BNtQZPqSIqShpAVv3?scode=AJEAIQdfAAoLG0A4eAAHoAEAbcACk&tab=fcujaj" target="_blank"><span style="line-height:2;">结果分析记录单</span></a><br />
    2. <a href="https://iwiki.woa.com/p/605728350" target="_blank"><span style="line-height:2;">启动自动化测试说明</span></a><br />
    
    <p>
        <br />
    </p>
    
    <footer class="footer">
        <div class="container-fluid">
            <HR>
            <span class="text-muted">
                Power by <a href="https://git.woa.com/u/ssfanli" target="_blank">@ssfanli</a>
            </span>
        </div>
    </footer>
"""

# table主干
# device_overview_rows, case_compare_title_rows, case_compare_detail_rows
TABLE_TMPL = """
    <h3> 一、设备概况 </h3>
    <table class="pure-table pure-table-bordered">
        <thead>
            <tr>
                <th>平台</th>
                <th>设备名</th>
                <th>设备号</th>
                <th>系统</th>
                <th>类型</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                %(device_overview_rows)s
            </tr>
        </tbody>
    </table>

    <h3> 二、对比详情 </h3>
    <table class="pure-table pure-table-bordered">
        <thead>
            <tr>
                %(case_compare_title_rows)s
            </tr>
        </thead>
        <tbody>
                %(case_compare_detail_rows)s
        </tbody>

    </table>

"""

# 设备概况行
# platform, model, os_version, datatype
TBODY_DEVICE_OVERVIEW_ROW_TMPL = """
                <td>{platform}</td>
                <td>{model}</td>
                <td>{device_id}</td>
                <td>{os_version}</td>
                <td>启动耗时测试</td>
"""

# case数据对比表 - 表头
# target_app_ver, current_app_ver
TBODY_CASE_COMPARE_TITLE_ROW_TMPL = """
                <th>场景</th>
                <th>视频拆帧</th>
                <th>耗时阶段</th>
                <th>商店[V{target_app_ver}]</th>
                <th>测试[V{current_app_ver}]</th>
                <th>增长率</th>
                <th>增长率阈值</th>
                <th>结果</th>
                <th>说明</th>
"""

# case数据对比表 - 第一行模板（2022/1/1更新）
# rowspan_num, case_id, case_name, img(list), case_compare_detail_row_content
TBODY_CASE_COMPARE_DETAIL_ROW_BODY_TMPL = """
                <tr>
                <td rowspan="3"><a href="https://perfdog.qq.com/case_detail/{case_id}" target="_blank">冷启动</a></td>
                <td rowspan="3">
                    <a onfocus='this.blur();' href="javacript:void(0);" onclick="show_img(this)">show</a>
                    <div class="screenshots"  style="display:none">
                        <a class="close_shots"  onclick="hide_img(this)"></a>
                        {case_img}
                        <div class="imgyuan"></div>
                    </div>
                </td>
                <td>真实耗时(ms)</td>
                <td>{index_target_value}</td>
                <td>{index_current_value}</td>
                <td><span style="color: {color}; ">{index_growth_rate}</span></td>
                <td>{threshold}</td>
                <td><span style="color: {color}; ">{index_result}</span></td>
                <td style="word-wrap:break-word;word-break:break-all;" width="280px";>{index_reason}</td>
                </tr>
"""

# case图片模板
# img_str
TBODY_CASE_IMG_TMPL = '<img src="data:image/jpg;base64,{}" style="display: none;" class="img"/>'

# case数据对比表 - 行内容
# index_name, index_target_value, index_current_value, color, index_growth_rate, threshold, index_result
TBODY_CASE_COMPARE_DETAIL_ROW_CONTENT_TMPL = """
                <td>{index_name}</td>
                <td>{index_target_value}</td>
                <td>{index_current_value}</td>
                <td><span style="color: {color}; ">{index_growth_rate}</span></td>
                <td>{threshold}</td>
                <td><span style="color: {color}; ">{index_result}</span></td>
                <td style="word-wrap:break-word;word-break:break-all;" width="280px";>{index_reason}</td>
"""

# case数据对比表 - 其他行模板
# case_compare_detail_row_content
TBODY_CASE_COMPARE_DETAIL_OTHER_ROW_TMPL = """
                <tr>
                {case_compare_detail_row_content}
                </tr>
"""

if __name__ == '__main__':

    d = {
        'rowspan_num': 3,
        'case_id': '123456',
        'case_name': '视频点播',
        'img': ['', ''],
        'index_details': [
            {'index_name': 'CPU(%)', 'index_target_value': 3.00, 'index_current_value': 4.00, 'color': 'green',
             'index_growth_rate': 3.12, 'threshold': [-30, 5], 'index_result': '正常'},
            {'index_name': 'MEM(MB)', 'index_target_value': 3.00, 'index_current_value': 4.00, 'color': 'green',
             'index_growth_rate': 3.12, 'threshold': [-30, 5], 'index_result': '正常'},
            {'index_name': 'FPS', 'index_target_value': 3.00, 'index_current_value': 4.00, 'color': 'green',
             'index_growth_rate': 3.12, 'threshold': [-30, 5], 'index_result': '异常'},
        ]
    }

    ds = [
        {
            'rowspan_num': 3,
            'case_id': '123456',
            'case_name': '视频点播',
            'img': ['', ''],
            'index_details': [
                {'index_name': 'CPU(%)', 'index_target_value': 3.00, 'index_current_value': 4.00, 'color': 'green',
                 'index_growth_rate': 3.12, 'threshold': [-30, 5], 'index_result': '正常'},
                {'index_name': 'MEM(MB)', 'index_target_value': 3.00, 'index_current_value': 4.00, 'color': 'green',
                 'index_growth_rate': 3.12, 'threshold': [-30, 5], 'index_result': '正常'},
                {'index_name': 'FPS', 'index_target_value': 3.00, 'index_current_value': 4.00, 'color': 'green',
                 'index_growth_rate': 3.12, 'threshold': [-30, 5], 'index_result': '异常'},
            ]
        },
        {
            'rowspan_num': 2,
            'case_id': '456789',
            'case_name': '移动直播',
            'img': ['', ''],
            'index_details': [
                {'index_name': 'CPU(%)', 'index_target_value': 3.00, 'index_current_value': 4.00, 'color': 'green',
                 'index_growth_rate': 3.12, 'threshold': [-30, 5], 'index_result': '正常'},
                {'index_name': 'MEM(MB)', 'index_target_value': 3.00, 'index_current_value': 4.00, 'color': 'green',
                 'index_growth_rate': 3.12, 'threshold': [-30, 5], 'index_result': '正常'},
            ]
        },

    ]

    case_compare_detail_row_contents = [TBODY_CASE_COMPARE_DETAIL_ROW_CONTENT_TMPL.format(**_) for _ in
                                        d.get('index_details')]
    res = ''
    for idx, content in enumerate(case_compare_detail_row_contents):
        if idx == 0:
            res += TBODY_CASE_COMPARE_DETAIL_ROW_BODY_TMPL.format(case_compare_detail_row_content=content, **d)
        else:
            res += TBODY_CASE_COMPARE_DETAIL_OTHER_ROW_TMPL.format(case_compare_detail_row_content=content)

    print(res)
