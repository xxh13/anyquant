from django.conf.urls import include, url
# from account.views import register
from django.contrib import admin
from quant_lab import views as quant_lab_views
from quant_lab import strategy_cate_views
from account import views as account_views
from quant_bbs import views as quant_bbs_views
from anyquant import views as anyquant_views
from quant_admin import views as quant_admin_views
from social import views as social_views
from quant_data import views as quant_data_views
from quant_stock.views import stock_urls

urlpatterns = (
    # Examples:
    # url(r'^$', 'quant_base.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += (
    url(r'^$', quant_lab_views.index),
    url(r'^labs/$', quant_lab_views.home),
    url(r'^labs/strategy/(?P<strategy_visit_id>\w+)$', quant_lab_views.labs),
    url(r'^algo/run/', quant_lab_views.run_algo),
    url(r'^editor/code_complete', quant_lab_views.code_complete),
    url(r'^editor/stock_complete', quant_lab_views.stock_complete),

    url(r'^strategy/new/$', quant_lab_views.new_strategy),
    url(r'^strategy/template/new/$', quant_lab_views.quant_template_save),
    url(r'^strategy/save$', quant_lab_views.save_strategy),
    url(r'^strategy/delete/$', quant_lab_views.delete_strategy),
    url(r'^ajax/strategy/valid/$', quant_lab_views.strategy_name_validation),

    url(r'^help$', quant_lab_views.quant_help),
)

urlpatterns += (
    url(r'^strategy/cate/new/$', strategy_cate_views.strategy_cate_new),
    url(r'^strategy/cate/update/$', strategy_cate_views.strategy_cate_update),
    url(r'^strategy/cate/delete/$', strategy_cate_views.strategy_cate_remove),
    url(r'^strategy/cate/movestrategy/$', strategy_cate_views.strategy_cate_strategy_move),
)

urlpatterns += (
    url(r'^register/', account_views.register),
    url(r'^login/', account_views.login),
    url(r'^logout/', account_views.logout),
    url(r'^account/active', account_views.account_active),

    url(r'^img/captcha/$', account_views.code),
)

urlpatterns += (
    url(r'^bbs/$', quant_bbs_views.bbs),
    url(r'^bbs/create', quant_bbs_views.bbs_create),
    url(r'^bbs/post/$', quant_bbs_views.bbs_submit),
    url(r'^bbs/search$', quant_bbs_views.bbs_search),
    url(r'^bbs/comment/(?P<comment_id>\w+)', quant_bbs_views.bbs_detail),
    url(r'^ajax/bbs/submit/$', quant_bbs_views.bbs_submit),
    url(r'^ajax/bbs/star/$', quant_bbs_views.bbs_star),
    url(r'^feedback/', quant_bbs_views.feedback),
    url(r'^bbs/profile/(?P<account_id>\w+)', quant_bbs_views.bbs_profile),

    url(r'^bbs/follow/$', quant_bbs_views.follow_user),
)

urlpatterns += (
    url('^api/pe', anyquant_views.api_pe),
    url('^api/sha300', anyquant_views.api_sha300),
    url('^api/stock/all', anyquant_views.api_all_stockcode),
    url('^api/stock/(?P<stock_code>[a-z]{2}[0-9]{6}$)', anyquant_views.api_specified_stock),

)

urlpatterns += (
    url(r'social/share/$', social_views.share),
    url(r'share/visit/(?P<share_code>\w+)', social_views.share_visit),
)

urlpatterns += (
    url(r'^admin/$', quant_admin_views.admin_home),
    url(r'^admin/bbs/$', quant_admin_views.admin_bbs_show),
    url(r'^admin/bbs_del$', quant_admin_views.admin_bbs_del),
    url(r'^admin/bbs_search$', quant_admin_views.admin_bbs_search),
    url(r'^admin/user/$', quant_admin_views.admin_user_show),
    url(r'^admin/user_search$', quant_admin_views.admin_user_search),
    url(r'^admin/user_del$', quant_admin_views.admin_user_del),
    url(r'^admin/strategy/$', quant_admin_views.admin_strategy_show),
    url(r'^admin/strategy_detail/(?P<strategy_id>\d+)', quant_admin_views.admin_strategy_detail),
    url(r'^admin/strategy_search/$', quant_admin_views.admin_strategy_search),
    url(r'^admin/strategy_del/$', quant_admin_views.admin_strategy_del),
)

urlpatterns += (
    url(r'stock/history_data$', quant_data_views.stock_data_all),
    url(r'stock/history_data_detail$', quant_data_views.stock_detail_basic)
)

urlpatterns += stock_urls
# urlpatterns = patterns(r'^register/', register)
