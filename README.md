# Descripción del Proyecto

Este proyecto es una tienda en línea innovadora que permite a los amantes de la música convertir sus playlists, canciones favoritas o álbumes en vinilos personalizados de alta calidad. A través de una plataforma intuitiva desarrollada en Django, los usuarios podrán seleccionar su contenido musical, personalizar el diseño de la carátula y etiquetas, y recibir su vinilo en casa.
La propuesta combina la nostalgia y el valor artístico del vinilo con la flexibilidad del consumo digital actual. Además, ofrece una experiencia única de personalización, permitiendo que cada cliente cree un producto exclusivo, ya sea para uso personal o como un regalo especial.
La plataforma no solo facilita la compra y diseño de los vinilos, sino que también gestiona la producción y logística de envíos, asegurando un servicio completo y sin complicaciones. Con esta propuesta, buscamos revivir el amor por el formato físico, brindando una forma tangible y sentimental de disfrutar la música en la era digital.

```
+---------------------+
|       User          |
+---------------------+
| id                  |
| username, email...  |
+---------------------+
          |
          | 1
          |
          | * 
+---------------------+
|       Order         |
+---------------------+
| id                  |
| total_price         |
| created_at          |
| status              |
+---------------------+
| user_id (FK)        |
+---------+-----------+
          |
          | 1
          | 
          | 1
+----------------------+
|      Shipping        |
+----------------------+
| id                   |
| tracking_number      |
| status               |
| estimated_delivery   |
+----------------------+
| order_id (OneToOne)  |
+----------------------+

          *
+---------------------+           * 
|       Vinyl         |<-------->|
+---------------------+          |
| id                  |          |
| name                |          |
| imageDesign         |          |
| size                |          |
| colour              |          |
| price               |          |
+---------------------+          |
          ^                      |
          |                      |
          |                      |
     +----+----------------------+
     |      OrderItem           |
     +--------------------------+
     | id                       |
     | quantity                 |
     | order_id (FK)            |
     | vinyl_id (FK)            |
     +--------------------------+

```
