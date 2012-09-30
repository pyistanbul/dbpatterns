Tastypie ile Django uygulamalarımızda kolayca REST prensiplerine göre web servisleri yazabiliyoruz. Hatta Sadece bir iki tanımlama ile Django modellerine REST arayüzü açıp, istersek de bu servisi istediğimiz gibi özelleştirebilmekteyiz.

Ancak tabii ki bu kolaylık sadece Django modelleri için geçerli. Eğer ORM olmayan bir kaynağa web servisi yazacaksanız kollarınızı sıvamanız gerekecek :) Bu blog yazısında MongoDB örneğini vereceğim.

MongoDB client'i olarak PyMongo'yu kullanacağız. PyMongo'yu aşağıdaki gibi pip ile yükleyebilirsiniz.

    pip install pymongo

PyMongo, MongoDB'nin python için implement edilmiş bir kütüphanesidir. Bu kütüphane ile Python üzerinden MongoDB ile istediğimiz gibi oynayabiliriz.

    from pymongo import Connection

    db = Connection().book # book adındaki veritabanını getirir, eğer yoksa oluşturur.
    documents = db.documents # documents adındaki koleksiyonu getirir, yoksa oluşturur.
                             # bunu ilişkisel veritabanlarındaki -tablo– olarak düşünebilirsiniz.
    documents.insert({
         "title": "selam"
    }) # koleksiyona yeni bir döküman ekler. bunu ise satır olarak düşünebilirsiniz.

    documents.find() # koleksiyondaki tüm dokümanları getirir.

Tastypie üzerinde özel bir resource (kaynak) oluşturmak için Resource ve ModelResource sınıflarını kullanırız. Biz Resource sınıfını kullanacağız. Zaten ModelResurce da aynı bizim yapacağımız MongoDB için yapacağımız gibi Django modelleri için implement edilmiş bir sınıftır.

Bu sınıfta aşağıdaki metodları ezmemiz gerekecek.

 - **obj_get**: Dökümanın detayına ulaşmak için.
 - **obj_get_list**: Dökümanın listesine ulaşmak için.
 - **obj_create**: Döküman eklemek için. HTTP POST metodu ile gelmemiz gerekir.
 - **obj_update**: Dökümanın güncellemek için. HTTP PUT metodu ile gelmemiz gerekir.
 - **obj_delete**: Dökümanın silmek için. HTTP DELETE metodu ile gelmemiz gerekir.

Bunun dışında bir de kaynak olarak kullanacağımız yapı için bir sınıf yazmamız gerekecek. Bunu model gibi düşünebilirsiniz. MongoDB'de bize dictionary benzeri bir sınıf yeterli olacaktır. Hatta bu sınıfı direkt olarak dictionary'den türetebiliriz.

    class Document(dict):
        # dictionary'deki öğelere direkt obje üzerinden attribute (özellik) olarak
        # erişmek için __getattr__ magic metodunu eziyoruz.
        def __getattr__(self, item):
            # dictionary'deki get metodunu kullanarak eğer öğe yoksa None gelmesini sağlıyoruz.
            return self.get(item)

Yukarıdaki MongoDB dökümanları için basit bir sınıf hazırladık. Bu işimizi görecektir. Ayrıca bu sınıfı daha kolay bir şekilde __getattr__ metodunu get metoduna eşitleyerek de tanımlayabiliriz. Çünkü dikkat ettiyseniz bu sınıfta farklı hiç bir şey yapmıyoruz.

    class Document(dict):
        __getattr__ = dict.get

Resource'umuzu yazmaya başlayabiliriz.

    from django.core.urlresolvers import reverse

    from bson import ObjectId
    from tastypie import fields
    from tastypie.resources import Resource


    class DocumentResource(Resource):

        # Resource üzerinde bulunacak field'ları ve bu field'ların MongoDB
        # üzerinde hangi kolonlarda bulunduğunu tanımlıyoruz.
        id = fields.CharField(attribute="_id")
        title = fields.CharField(attribute="title")
        entities = fields.ListField(attribute="entities", null=True)

        class Meta:
            resource_name = "documents" # endpoint'imizin adı
            list_allowed_methods = ["get", "post"]
            detail_allowed_methods = ["get", "put", "delete"]
            authorization = Authorization()
            object_class = Document # hazırladığımız dictionary benzeri sınıf


        def obj_get_list(self, request=None, **kwargs):
            # documents koleksiyonundaki tüm dökumanları alıp her dökumanı
            # hazırladığımız Document sınıfının objesine çeviriyoruz.
            return map(Document, db.documents.find())

        def obj_get(self, request=None, **kwargs):
            # dökumanın ID'sini BSON formatına çevirip MongoDB'ye sorgulatıyoruz.
            # dönen dökumanı Document objesine çeviriyoruz.
            return Document(db.documents.find_one({ "_id": ObjectId(kwargs.get("pk")) }))

        def obj_create(self, bundle, **kwargs):
            # POST ile gelen datayı direkt olarak MongoDB üzerine yazıyoruz.
            # tanımladığımız field'lar dışındaki verileri tastypie yoksayar.
            db.documents.insert(bundle.data)
            return bundle

        def obj_update(self, bundle, request=None, **kwargs):
            # dökumanın id'sini BSON formatına çevirip güncelleme işlemi yaptırıyoruz.
            # buradaki $set parametresi dönen dökümanın sadece belirli alanlarını
            # güncelleyebilmemizi sağlar.
            db.documents.update({"_id": ObjectId(kwargs.get("pk")) }, { "$set": bundle.data })
            return bundle

        def obj_delete(self, request=None, **kwargs):
            # parametre olarak gelen id'ye göre dökumanı siliyoruz.
            db.documents.remove({ "_id": ObjectId(kwargs.get("pk")) })

        def get_resource_uri(self, item):
            # bu metod dökumanın ulaşılacağı URI'i belirler.
            # item parametresi detay sayfalarında Bundle, list sayfalarında ise
            # Document objesi olarak geliyor. Bunu kontrol ettikten sonra
            # Django'nun reverse fonksiyonu ile url'imizi sorguluyoruz.
            pk = item.obj._id if isinstance(item, Bundle) else item._id
            return reverse("api_dispatch_detail", kwargs={
                "resource_name": self._meta.resource_name,
                "pk": pk
            })


Resource'umuzu bu şekilde tanımlamış olduk. Artık aşağıdaki gibi urls.py'mize ekleyerek çalıştırabiliriz.

    from django.conf.urls import include, patterns

    from documents.resources import DocumentResource

    urlpatterns = patterns('',

        (r'^api/', include(DocumentResource().urls)),

    )

Ayrıca REST API'ınızı test etmek için httpie aracını kullanabilirsiniz.



- **obj_get**: Dökümanın detayına ulaşmak için.
- **obj_get_list**: Dökümanın listesine ulaşmak için.
- **obj_create**: Döküman eklemek için. HTTP POST metodu ile gelmemiz gerekir.
- **obj_update**: Dökümanın güncellemek için. HTTP PUT metodu ile gelmemiz gerekir.
- **obj_delete**: Dökümanın silmek için. HTTP DELETE metodu ile gelmemiz gerekir.


<table>
    <tr>
        <th>obj_get</th>
        <td>Dökümanın detayına ulaşmak için.</td>
    </tr>
    <tr>
        <th>obj_get_list</th>
        <td>Dökümanın listesine ulaşmak için.</td>
    </tr>
    <tr>
        <th>obj_create</th>
        <td>Döküman eklemek için. HTTP POST metodu ile gelmemiz gerekir.</td>
    </tr>
    <tr>
        <th>obj_update</th>
        <td>Dökümanın güncellemek için. HTTP PUT metodu ile gelmemiz gerekir.</td>
    </tr>
    <tr>
        <th>obj_delete</th>
        <td>Dökümanın silmek için. HTTP DELETE metodu ile gelmemiz gerekir.</td>
    </tr>
</table>