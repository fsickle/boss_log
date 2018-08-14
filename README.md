<h2>模拟登陆boss直聘网站</h2>
<p>从 boss直聘登陆页面可得到验证码的 key,通过它下载得到验证码,识别后输入验证码值</p></br>
<p>(尝试使用 tesserocr 识别验证码失败后，采用人脸识别)</p><br>
<p>输入得到验证码后，会发送验证码到手机。输入之后即可完成登陆。结果如下：</P>
<img src='result/result1.png'>
<p>用于<stong>多线程</stong>，将热门职业和最新职业的所有结果存储到 mongodb,如图：</P>
<img src='result/result3.png'>
<p>对爬取到的数据查询，可以得到在描述中带有‘爬虫’关键字的的具体数据，如图所示:</p>
<img src="result/result4.png">
<p>尽量采用<strong>代理 ip</strong> 进行爬取</P>
<p>对于够烂的ip别忘了添加requests的请求次数</P>