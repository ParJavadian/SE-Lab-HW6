## پیاده‌سازی

در این معماری، یک سرویس با عنوان service1 داریم که از عملیات‌های post , get روی یک پایگاه داده‌ی ساده پشتیبانی می‌کند. برای دسترسی به سرویس، باید درخواست‌ها از طریق endpoint آدرس /item به interface فرستاده شوند. سپس این واسط، درخواست را به سرویس nginx که برای load balancing استفاده شده است ارسال کرده، پاسخ آن را دریافت کرده و به درخواست‌کننده ارسال می‌کند.

برای load balancing، ابتدا ۳ replica از سرویس خود را تعریف می‌کنیم. سپس در کانفیگ nginx لود را بین سرویس‌ها توزیع کرده و به سمت backend ارسال می‌کنیم. برای کنترل فشار روی سرویس‌ها هم می‌توانیم از الگوریتم‌های بهینه مانند least_conn که درخواست را به سمت سروری که کمترین لود را دارد ارسال می‌کند، استفاده کنیم.

در هر دوی پوشه‌ها، requirement هایی که کد به آن‌ها وابسته است را در فایل requirements.txt قرار داده و در Dockerfile از لود شدن صحیح آن‌ها قبل از شروع اجرای برنامه اطمینان می‌یابیم.

در انتها، تمام کانتینرها را در docker-compose.yml به هم متصل می‌کنیم. تمام این کانتینرها روی شبکه‌ی app_network بالا خواهند بود و نیازمندی‌های آن‌ها به هم را هم در این فایل مشخص می‌کنیم. همچنین پایگاه داده‌ی ما که در backend درخواست‌ها به آن ارسال می‌شوند، یک کانتینر مشترک postgres است که تنظیمات آن را در این فایل انجام داده و روی پورت 5432 بالا می‌آوریم.

نهایتاً سرویس ما روی localhost با پورت 8080 قابل دسترسی خواهد بود. برای تست آن، کافیست ابتدا ۳ درخواست post به آن ارسال کنیم و سپس با ارسال یک درخواست get، تمام داده‌هایی که ارسال کرده بودیم را ببینیم. این کار از طریق نرم‌افزار postman انجام شده و نتایج آن در تصاویر زیر قابل مشاهده است:

![
](<images/Screenshot 2024-12-06 at 8.21.56 PM.png>) ![
](<images/Screenshot 2024-12-06 at 8.22.10 PM.png>)

پس از ارسال این ۴ درخواست، می‌توانیم با بررسی لاگ‌های سرورها متوجه شویم که درخواست‌ها به طور یکنواختی بین آن‌ها توزیع شده‌اند:

![
](<images/Screenshot 2024-12-06 at 8.22.43 PM.png>) ![
](<images/Screenshot 2024-12-06 at 8.22.49 PM.png>) ![
](<images/Screenshot 2024-12-06 at 8.22.55 PM.png>)

همچنین با اجرای دستورات docker container ls , docker image ls می‌توانیم وجود سرویس‌های خود را ببینیم:

![
](<images/Screenshot 2024-12-06 at 8.24.22 PM.png>)

## پاسخ سوالات پایانی

**1. مفهوم stateless چیست و استفاده از این مفهوم در آزمایش چه معنایی دارد؟**

سیستم‌های stateless به این معنا هستند که هیچ اطلاعاتی از وضعیت (State) مشتری یا درخواست قبلی را در خود نگه نمی‌دارند. هر درخواست ورودی به صورت مستقل از درخواست‌های دیگر پردازش می‌شود.
در این آزمایش، معماری RESTful که برای پیاده‌سازی API استفاده شده است ذاتاً stateless است. این بدین معناست که هر درخواست HTTP به طور مستقل و بدون نیاز به نگه‌داری اطلاعات جلسه (Session) پردازش می‌شود.
استفاده از این معماری باعث ساده‌تر شدن مدیریت سرویس‌ها در محیط‌های توزیع‌شده مانند Docker می‌شود.


**2.در مورد تفاوت‌های load balancing در لایه ۴ و ۷ از مدل OSI مطالعه کرده و مزیت‌های آن‌ها نسبت به یکدیگر را مختصر توضیح دهید. شما در این آزمایش از load balancing در کدام لایه استفاده کردید؟**

در معماری شبکه، Load Balancing می‌تواند در لایه ۴ یا لایه ۷ از مدل OSI انجام شود:  

**لایه ۴ (Transport Layer):** در این روش، ترافیک بر اساس اطلاعاتی مانند آدرس IP و پورت توزیع می‌شود. Load Balancer فقط داده‌های شبکه را پردازش می‌کند و محتوای درخواست‌ها (مانند نوع فایل یا URL) را بررسی نمی‌کند. این روش سریع‌تر است، زیرا به پردازش محتوای درخواست نیازی ندارد، اما انعطاف‌پذیری کمتری دارد و نمی‌تواند تصمیم‌گیری بر اساس داده‌های لایه کاربرد انجام دهد.  

**لایه ۷ (Application Layer):** در این روش، ترافیک بر اساس محتوای درخواست (مانند هدرهای HTTP، URL، یا نوع داده) توزیع می‌شود. این نوع Load Balancing انعطاف‌پذیری بیشتری دارد و امکان پیاده‌سازی سیاست‌های پیچیده‌تر مانند مسیریابی به‌خصوص برای انواع خاصی از درخواست‌ها را فراهم می‌کند. اما به دلیل پردازش بیشتر، منابع بیشتری مصرف می‌کند و ممکن است تأخیر بیشتری داشته باشد.  

در این آزمایش از Load Balancing در **لایه ۷** استفاده شده است، زیرا NGINX به‌عنوان Load Balancer مورد استفاده قرار گرفته که قادر به مدیریت و توزیع ترافیک HTTP در سطح Application Layer است. این امکان به ما داده تا درخواست‌ها را بر اساس الگوریتم‌های مختلف، از جمله **Least Connections**، بین سه Replica از سرویس توزیع کنیم.
