![](https://cdn.nlark.com/yuque/0/2023/jpeg/23202369/1699157301044-98177f6d-ef18-494a-925e-10e22383d921.jpeg)
<a name="VUUG3"></a>
### Regression 回归
<a name="Q2dTU"></a>
#### cost function
![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699093710329-39af6d62-da83-4c37-b715-3cc9962ba2d4.png#averageHue=%23eeeeee&clientId=ud111d2b7-09ec-4&from=paste&height=153&id=u1689b047&originHeight=306&originWidth=402&originalType=binary&ratio=2&rotation=0&showTitle=false&size=51469&status=done&style=none&taskId=u761a76dd-6826-401c-a0b7-08aeadc1035&title=&width=201)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699093857716-62572b43-8d5a-466f-8b14-d6c8ef1d3b16.png#averageHue=%23f8f8f7&clientId=ud111d2b7-09ec-4&from=paste&height=115&id=u533b3514&originHeight=424&originWidth=2090&originalType=binary&ratio=2&rotation=0&showTitle=false&size=384401&status=done&style=none&taskId=uae83a66d-7576-474b-8b63-580687e855a&title=&width=565)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699520885993-0f8fe278-7d96-4bc6-8a10-557298ed7c62.png#averageHue=%23f0f0f0&clientId=u5588a079-0921-4&from=paste&height=215&id=ucbc76f11&originHeight=430&originWidth=690&originalType=binary&ratio=2&rotation=0&showTitle=false&size=58615&status=done&style=none&taskId=u719135bf-4072-47a2-a854-8745cdf8775&title=&width=345)
<a name="duWiU"></a>
#### gradient descent 梯度下降
<a name="ugYC0"></a>
##### 梯度下降算法的计算方式
![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699094466891-069d2916-3ab6-4b70-92d9-03f6961c6195.png#averageHue=%23fcf8e7&clientId=ud111d2b7-09ec-4&from=paste&height=284&id=ub47022cb&originHeight=646&originWidth=1143&originalType=binary&ratio=2&rotation=0&showTitle=false&size=497616&status=done&style=none&taskId=uc7eed77e-7985-4b07-9e76-51cdd464b5f&title=&width=502.49310302734375)

<a name="KktTQ"></a>
##### 梯度下降算法中 导数的作用
初始值为左上的取值时，w' = w - α *d [J(w)]  在左上点上的导数值（正数），w' 变小，w' 向更小的值下降<br />初始值为左下的取值时，w' = w - α *d [J(w)]  在左下点上的导数值（负数），w' 变大，w' 向更大的值下降<br />=> w 向使 J(w) 变小的趋势变化<br />=> 当 w 向最理想值趋势变化时，每 step 的变化都将变得越来越小（α固定），体现出梯度的特性<br />=> batch gradient descent ：each step of gradient descent uses all the training examples. (other gradient descent: subsets)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699099456621-3e07baac-7da7-4ce8-a7c4-755a4c7504fd.png#averageHue=%23fdfcfc&clientId=ud111d2b7-09ec-4&from=paste&height=260&id=u6aadefc0&originHeight=568&originWidth=1023&originalType=binary&ratio=2&rotation=0&showTitle=false&size=219589&status=done&style=none&taskId=ube95f744-47f9-4987-8789-cbcc111725f&title=&width=467.49658203125)

<a name="EkUWj"></a>
##### <br />
![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699105382311-d1f83ce8-009b-48fe-b285-6361648d9726.png#averageHue=%23fafafa&clientId=ud111d2b7-09ec-4&from=paste&height=239&id=u00b72717&originHeight=870&originWidth=1677&originalType=binary&ratio=2&rotation=0&showTitle=false&size=475551&status=done&style=none&taskId=u2553c73c-c78d-48ef-a133-34bb584b333&title=&width=460.11285400390625)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699353830561-bf2938ff-e03b-4209-9d29-0c122a9c8e56.png#averageHue=%23f5f5f5&clientId=u5588a079-0921-4&from=paste&height=148&id=NbcG5&originHeight=296&originWidth=618&originalType=binary&ratio=2&rotation=0&showTitle=false&size=51314&status=done&style=none&taskId=ufd9c2408-220d-4297-9ea9-14ecd94bc66&title=&width=309)

求导的过程 ↓<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699105433119-4af2de2f-45f2-47f5-90e2-3ee5e608411c.png#averageHue=%23f8f1e7&clientId=ud111d2b7-09ec-4&from=paste&height=241&id=ue2366d7b&originHeight=634&originWidth=1144&originalType=binary&ratio=2&rotation=0&showTitle=false&size=472498&status=done&style=none&taskId=ub281e2d2-0fbc-4f13-94d8-0fbccf1f96a&title=&width=433.99658203125)
<a name="Op034"></a>
##### learning rate 学习率
![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699521502209-e20910be-eb60-49a4-a20a-b6e430522c59.png#averageHue=%23f1f1f0&clientId=u5588a079-0921-4&from=paste&height=237&id=u479524a7&originHeight=620&originWidth=1312&originalType=binary&ratio=2&rotation=0&showTitle=false&size=152447&status=done&style=none&taskId=ud900b020-d43f-4b90-8d4c-d28bd232334&title=&width=502)
<a name="hD49r"></a>
#### multiple linear regression 多元线性回归
![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699521666983-2537c7d6-39c5-4e32-970c-0280cb824690.png#averageHue=%23fdfcfa&clientId=u5588a079-0921-4&from=paste&height=53&id=uf4cfe95e&originHeight=142&originWidth=1042&originalType=binary&ratio=2&rotation=0&showTitle=false&size=61424&status=done&style=none&taskId=ud73e243c-da38-4ad7-a125-1cb2c38ac97&title=&width=386)
<a name="fbgRz"></a>
##### vectorization 向量化
![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699521701708-9e18d822-a01a-4a55-92fc-15558c73dfd0.png#averageHue=%23f8f7f6&clientId=u5588a079-0921-4&from=paste&height=186&id=uec9953f1&originHeight=742&originWidth=1670&originalType=binary&ratio=2&rotation=0&showTitle=false&size=360770&status=done&style=none&taskId=uac2f765d-a667-4834-99c7-681c677d937&title=&width=418)![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699522760138-258475ca-bb77-4782-a36a-e677b3179e03.png#averageHue=%23f7f7f7&clientId=u5588a079-0921-4&from=paste&height=227&id=u5f446a8d&originHeight=894&originWidth=1738&originalType=binary&ratio=2&rotation=0&showTitle=false&size=560906&status=done&style=none&taskId=u2e779f3d-2d97-4c5b-b401-a66a957be28&title=&width=441.99658203125)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1699522787498-2c0bc3e3-c6f2-46a6-8e7f-a6243a841518.png#averageHue=%23f5f3e8&clientId=u5588a079-0921-4&from=paste&height=224&id=ue4c22758&originHeight=900&originWidth=1758&originalType=binary&ratio=2&rotation=0&showTitle=false&size=615576&status=done&style=none&taskId=ud68e37c9-6be8-4fc1-a439-941aedfddc5&title=&width=437.99481201171875)
<a name="LSHfm"></a>
#### feature scaling 特征缩放
作用：<br />使梯度下降运行的更快<br />背景：<br />不同的特征，取值范围非常不同时，可能会导致梯度下降运行缓慢，此时需要缩放不同的特征，使它们都能在可比较的取值范围<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700474465182-cee34066-dfb5-424c-a4c7-303f5c485a8f.png#averageHue=%23f7f5f3&clientId=uf755e7e9-9680-4&from=paste&height=138&id=uf73ece1b&originHeight=518&originWidth=722&originalType=binary&ratio=2&rotation=0&showTitle=false&size=116269&status=done&style=none&taskId=u9b3b7885-7337-4ad1-ac1c-5fc293eebdc&title=&width=193)与垂直轴想比，水平轴的比例或值范围更大<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700474540493-1f546e63-1ecf-4555-bbcd-4bed638278b6.png#averageHue=%23f7f7f7&clientId=uf755e7e9-9680-4&from=paste&height=147&id=u0a85e60f&originHeight=508&originWidth=834&originalType=binary&ratio=2&rotation=0&showTitle=false&size=159612&status=done&style=none&taskId=uedf3d2c3-8076-4956-a2eb-3ad2717b7bf&title=&width=241) cost function 的等高线图，水平轴的范围要窄得多，说明w1的一个非常小的变化也会对预估结果产生非常大的影响，相对而言，w2需要更大的变化才能是预测值产生明显的变化<br />影响：<br />瘦长型的等高线，梯度下降可能会在它最终找到全局最小值之前来回弹跳很长时间<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700475474303-640d1db1-b644-444e-b3d7-74c1489920d1.png#averageHue=%23f6f5f5&clientId=uf755e7e9-9680-4&from=paste&height=161&id=u4c4fcf77&originHeight=422&originWidth=926&originalType=binary&ratio=2&rotation=0&showTitle=false&size=174742&status=done&style=none&taskId=u1cbbc455-674b-43f9-9cc1-0dbf4e5f0cb&title=&width=352.4392395019531)<br />解决方案：<br />对数据进行一些转换，重新标度x1和x2，使彼此在可比较的范围，梯度下降可以找到一条更直接通往全局最小值的路径<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700476065062-f4f55800-08b2-49e3-928c-eb879294c962.png#averageHue=%23f3f2f1&clientId=uf755e7e9-9680-4&from=paste&height=203&id=u1e2352ea&originHeight=366&originWidth=1522&originalType=binary&ratio=2&rotation=0&showTitle=false&size=225663&status=done&style=none&taskId=uffc3a7d4-8573-4fd4-900c-805058202f1&title=&width=845.5555779551288)
<a name="Nq60W"></a>
##### 除以最大值
![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700477216803-d7d584d4-8aae-495e-8658-d0cf5e07cc27.png#averageHue=%23f9f7f4&clientId=uf755e7e9-9680-4&from=paste&height=195&id=u3651823d&originHeight=776&originWidth=1622&originalType=binary&ratio=2&rotation=0&showTitle=false&size=368316&status=done&style=none&taskId=u23e45912-22fa-4124-a74c-cc15afb52b9&title=&width=407.11285400390625)
<a name="CrV9U"></a>
##### mean normalization 均值归一化
求训练集上每个feature的平均值，记为μ<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700477848074-eb585b30-c762-4587-bf32-0f3b5ec88d1f.png#averageHue=%23f6f4f2&clientId=uf755e7e9-9680-4&from=paste&height=238&id=u73f4ae64&originHeight=870&originWidth=1694&originalType=binary&ratio=2&rotation=0&showTitle=false&size=465567&status=done&style=none&taskId=u18c36c15-5df3-4d17-a32a-2e91db92d26&title=&width=463.109375)

<a name="OuFWy"></a>
##### z-score normalization
σ：standard deviation 标准方差<br />μ：平均值<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700478942448-28af37af-daa6-406e-af96-74783c877bc0.png#averageHue=%23f6f4f2&clientId=uf755e7e9-9680-4&from=paste&height=220&id=uc65af972&originHeight=882&originWidth=1736&originalType=binary&ratio=2&rotation=0&showTitle=false&size=473686&status=done&style=none&taskId=u93c12c4d-3d36-49e2-b855-518873896ee&title=&width=433.107666015625)<br />缩放后的特征值需要在合理的范围内，否则都将降低梯度下降的效率<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700479151670-aa794030-71f0-4b83-b62d-79812e5a92b5.png#averageHue=%23f8f5f5&clientId=uf755e7e9-9680-4&from=paste&height=225&id=u229f3ffc&originHeight=758&originWidth=1508&originalType=binary&ratio=2&rotation=0&showTitle=false&size=448869&status=done&style=none&taskId=u2ec0f123-24f9-40f3-938e-d91bffe3389&title=&width=448.11285400390625)

<a name="QSKaF"></a>
#### 验证梯度下降是否收敛
横轴：迭代次数<br />纵轴：J(w_向量_,b)<br />曲线：**learning curve 学习曲线**<br />图：显示成本J在每次梯度下降迭代后的变化情况，与w,b 每次迭代的变化无关<br />判断：

- J 应该在每次迭代后减少
- J 在一次迭代后增加，通常意味着α过大，或代码存在错误
- 需要迭代的次数根据不同场景会有很大差别，eg：30，1,000-100,000
- automatic convergence test（自动收敛测试）
   - 比较难决定𝞮 取值，左图会有一个更清晰的显示

![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700493269257-6cf93d50-e7b5-4a52-9889-0ff20f0f0cf1.png#averageHue=%23f1f0ef&clientId=u8c8ccefa-15b1-4&from=paste&height=417&id=ub4ab4dfa&originHeight=750&originWidth=1744&originalType=binary&ratio=1.7999999523162842&rotation=0&showTitle=false&size=574614&status=done&style=none&taskId=u37952d39-badc-46b6-9806-b2b4d1cf68a&title=&width=968.8889145556798)


<a name="VYsbn"></a>
#### choosing  learning rate 

1. α 过大
   1. 会导致每次迭代时导数值偏差太大，J(w向量,b) 的值起起伏伏（坐上）
   2. 显示一条向上趋势的线（右上），这种场景也有可能是代码bug造成的
2. α过小
   1. 迭代效效率

![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700493884532-9fe78928-16df-42bc-9781-23ffd97e3006.png#averageHue=%23efecec&clientId=uadea92f2-e193-4&from=paste&height=307&id=ueddfb3b0&originHeight=890&originWidth=1732&originalType=binary&ratio=1.7999999523162842&rotation=0&showTitle=false&size=684512&status=done&style=none&taskId=u5ff12c5b-fcc4-4c77-a55c-5076d3762a3&title=&width=598.1128540039062)<br />调试tip：

1. 在足够小的α下，J 仍然在每次迭代中都成下降趋势，确认梯度下降的功能运行正常
2. 0.001 -> 0.003 -> 0.01 -> 0.03 -> 0.1 -> 0.3

![image.png](https://cdn.nlark.com/yuque/0/2023/png/23202369/1700494575000-f23ce0a7-2862-4bb8-9210-9f9a4ea69db2.png#averageHue=%23faf8f8&clientId=uadea92f2-e193-4&from=paste&height=205&id=uaa7c9790&originHeight=814&originWidth=1592&originalType=binary&ratio=1.7999999523162842&rotation=0&showTitle=false&size=388067&status=done&style=none&taskId=u1b05f68f-5990-4a5e-b68d-c3eb76ae54d&title=&width=401.11285400390625)

<a name="E5zRB"></a>
#### feature engineering 特征工程
Using intuition to design new features, by transforming or combining original features.<br />利用对问题的知识来设计新的特征，通常是通过转换或组合问题的原始特征来使学习算法更容易做出准确的预测

<a name="ZKPkA"></a>
#### Polynomial regression 多项式回归

<a name="tdmap"></a>
### Classification 
binary classfication 二元分类
<a name="pRxir"></a>
###  Logistic Regression 逻辑回归
sigmoid function<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/23202369/1711961589740-a24c3288-7840-4469-aff3-818f9f6d61f9.png#averageHue=%23f2f0f0&clientId=u127b2476-6096-4&from=paste&height=328&id=u2341287a&originHeight=590&originWidth=548&originalType=binary&ratio=1.7999999523162842&rotation=0&showTitle=false&size=125387&status=done&style=none&taskId=uf069cde2-673b-450d-960c-f4d17bd7041&title=&width=304.4444525094682)<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/23202369/1711962011461-6ccbb000-3a91-448d-b3c3-fba072721ae8.png#averageHue=%23f6f6f5&clientId=u127b2476-6096-4&from=paste&height=270&id=u55900fd6&originHeight=486&originWidth=1092&originalType=binary&ratio=1.7999999523162842&rotation=0&showTitle=false&size=186949&status=done&style=none&taskId=u60b18379-3c34-4d89-9ba8-96a40889827&title=&width=606.6666827378453)

<a name="NVEk8"></a>
#### overfitting/underfitting 过拟合/欠拟合
![image.png](https://cdn.nlark.com/yuque/0/2024/png/23202369/1711962596271-40648be3-0b2c-4bc9-97fe-90f787d904c3.png#averageHue=%23f3f2f2&clientId=u127b2476-6096-4&from=paste&height=301&id=u66507189&originHeight=542&originWidth=1196&originalType=binary&ratio=1.7999999523162842&rotation=0&showTitle=false&size=274807&status=done&style=none&taskId=u8fbb8489-edb0-4506-a464-79a984a07da&title=&width=664.4444620462116)<br />![image.png](https://cdn.nlark.com/yuque/0/2024/png/23202369/1711962679758-b9b5bc6f-69b5-4939-80ff-03f462d824e4.png#averageHue=%23f4f8f0&clientId=u127b2476-6096-4&from=paste&height=442&id=u9687383b&originHeight=796&originWidth=1260&originalType=binary&ratio=1.7999999523162842&rotation=0&showTitle=false&size=727252&status=done&style=none&taskId=u4d2eb0d1-ef68-4198-bac6-219b9cd2c22&title=&width=700.0000185436678)



<a name="Oma0L"></a>
### toolkit
[numpy](https://numpy.org/doc/stable/)<br />[scikit-learn](https://scikit-learn.org/stable/index.html)
<a name="Yd30q"></a>
#### 
