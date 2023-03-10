
#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#############################################

#############################################
# İş Problemi
#############################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.


#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı


#############################################
# PROJE GÖREVLERİ
#############################################

#############################################
# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
df = pd.read_csv(r"C:\Users\Gizem\PycharmProjects\pythonProject6\python_alistirma\persona.csv")

warnings.filterwarnings("ignore", category=FutureWarning)

df.head()
df.shape
df.info()
# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()
# Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?


df["COUNTRY"].value_counts()

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby(["COUNTRY"]).agg({"PRICE": "sum"})


# Soru 7: SOURCE türlerine  göre satış sayıları nedir?

# df.groupby(["SOURCE"]).agg({"PRICE": "count"})

df["SOURCE"].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?

df.groupby(["COUNTRY"]).agg({"PRICE": "mean"})


# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby(["SOURCE"]).agg({"PRICE": "mean"})

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE": "mean"})

#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################
df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"})

#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.

agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)
#ascending=False  Bu parametrenin varsayılan değeri "True" olduğundan, verilerin sıralama yönü varsayılan olarak artan (ascending) şekildedir.



#############################################
# GÖREV 4: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()
# agg_df.reset_index(inplace=True)
agg_df = agg_df.reset_index()


#############################################
# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'

agg_df["AGE"].max()
agg_df["AGE"].min()

agg_df["NEW_AGE"] = pd.cut(agg_df["AGE"], bins=[0,18,23,30,40, +df["AGE"].max()],
                           labels= ["0_18", "19_23", "24_30", "31_40", "41_"+ str(agg_df["AGE"].max())])
agg_df.head()

#############################################
# GÖREV 6: Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
# customers_level_based adında bir değişken tanımlayınız ve veri setine bu değişkeni ekleyiniz.
# list comp ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18
# Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.
agg_df["AGE"].max()
agg_df["AGE"].isnull().sum()
agg_df.info()

agg_df["customers_level_based"] = ["_".join([str(val).upper() for val in row[:3]] +
                                            [str(row[5]).upper()]) for row in agg_df.values]

agg_df.head()
agg_df["customers_level_based"].value_counts()

agg_df = agg_df.groupby(["customers_level_based"]).agg({"PRICE":"mean"})
agg_df=agg_df.reset_index()
agg_df.head()
agg_df["customers_level_based"].value_counts()

#############################################
# GÖREV 7: Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################

# PRICE'a göre segmentlere ayırınız,
df
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz,

# segmentleri betimleyiniz,
agg_df["PRICE"].describe()

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], q=4, labels=["Low", "Medium", "High","Very High"])
agg_df.head()
# segmentleri betimleyiniz,
agg_df["SEGMENT"].value_counts()



#############################################
# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################

# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_customer= "TUR_ANDROID_FEMALE_31_40"

agg_df[agg_df["customers_level_based"] == new_customer]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

new_customer0= "FRA_IOS_FEMALE_31_40"

agg_df[agg_df["customers_level_based"] == new_customer0]

