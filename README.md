<h2>尝试模拟登陆boss直聘网站</h2>
<p>从 boss直聘登陆页面可得到验证码的 key,通过它下载得到验证码,识别后输入验证码值</p></br>
<p>(尝试使用 tesserocr 识别验证码失败后，采用人脸识别)</p><br>
<p>输入得到验证码后，会发送验证码到手机。输入之后即可完成登陆。结果如下：</P>
<img src='result/result1.png'>
<p>爬虫会对成都的python岗位进行爬取，对爬取速度进行限制后，爬取到近200条数据后，会出现爬取为空的现象。结果如下：</p>
<img src='result/result2.png'>
<p>将结果存储到 mongodb,如图：</P>
<img src='result/result3.png'>