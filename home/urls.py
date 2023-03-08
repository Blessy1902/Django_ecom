from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path("cart/",views.cart, name='cart'),
    path("login/",views.login, name='login'),
    path("signup/",views.signup, name='signup'),
    # path("addpost/",views.AddPost.as_view(),name='addproduct'),
    # path('productsview/<int:product_id>/',views.product_detail,name='product_detail'),
    path("productview/<int:id>",views.productview, name='productview'),
    path("additems/",views.AddItems, name="additems"),
    path("logout", views.logout_request, name= "logout"),
    path("viewproduct/<int:id>", views.productview, name= "viewproduct"),
    path("product-edit/<int:id>", views.editproduct , name="editproduct"),
    path("product-editsave/", views.editproductsave ),
    path("product-delete/<int:id>", views.deleteproduct ),
    path("search/", views.search, name="search"),



    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>', views.order, name='order'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update-cart'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)