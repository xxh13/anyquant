from django.conf.urls import patterns, include, url
# from account.views import register
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quant_base.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('quant_lab.views',
    url(r'^$', 'index'),
    url(r'^labs/$', "home"),
    url(r'^labs/strategy/(?P<strategy_visit_id>\w+)$', 'labs'),
    url(r'^algo/run/', 'run_algo'),
    url(r'^editor/code_complete', 'code_complete'),
    url(r'^editor/stock_complete', 'stock_complete'),

    url(r'^strategy/new/$', 'new_strategy'),
    url(r'^strategy/template/new/$', 'quant_template_save'),
    url(r'^strategy/save$', 'save_strategy'),
    url(r'^strategy/delete/$', 'delete_strategy'),
    url(r'^ajax/strategy/valid/$', 'strategy_name_validation'),

    url(r'^help$', 'quant_help'),
)

urlpatterns += patterns('quant_lab.strategy_cate_views',
    url(r'^strategy/cate/new/$', 'strategy_cate_new'),
    url(r'^strategy/cate/update/$', 'strategy_cate_update'),
    url(r'^strategy/cate/delete/$', 'strategy_cate_remove'),
    url(r'^strategy/cate/movestrategy/$', 'strategy_cate_strategy_move'),
)

urlpatterns += patterns('account.views',
    url(r'^register/', 'register'),
    url(r'^login/', 'login'),
    url(r'^logout/', 'logout'),
    url(r'^account/active', 'account_active'),

    url(r'^img/captcha/$', 'code'),
)

urlpatterns += patterns('quant_bbs.views',
    url(r'^bbs/$', 'bbs'),
    url(r'^bbs/create', 'bbs_create'),
    url(r'^bbs/post/$', 'bbs_submit'),
    url(r'^bbs/search$', 'bbs_search'),
    url(r'^bbs/comment/(?P<comment_id>\w+)', 'bbs_detail'),
    url(r'^ajax/bbs/submit/$', 'bbs_submit'),
    url(r'^ajax/bbs/star/$', 'bbs_star'),
    url(r'^feedback/', 'feedback'),
    url(r'^bbs/profile/(?P<account_id>\w+)','bbs_profile'),

    url(r'^bbs/follow/$', 'follow_user'),
)

urlpatterns += patterns('anyquant.views',
    url('^api/pe', 'api_pe'),
    url('^api/sha300', 'api_sha300'),
    url('^api/stock/all', 'api_all_stockcode'),
    url('^api/stock/(?P<stock_code>[a-z]{2}[0-9]{6}$)', 'api_specified_stock'),

)

urlpatterns += patterns('social.views',
    url(r'social/share/$', 'share'),
    url(r'share/visit/(?P<share_code>\w+)', 'share_visit'),
)

urlpatterns += patterns('quant_admin.views',
    url(r'^admin/$', 'admin_home'),
    url(r'^admin/bbs/$', 'admin_bbs_show'),
    url(r'^admin/bbs_del$', 'admin_bbs_del'),
    url(r'^admin/bbs_search$', 'admin_bbs_search'),
    url(r'^admin/user/$', 'admin_user_show'),
    url(r'^admin/user_search$', 'admin_user_search'),
    url(r'^admin/user_del$', 'admin_user_del'),
    url(r'^admin/strategy/$', 'admin_strategy_show'),
    url(r'^admin/strategy_detail/(?P<strategy_id>\d+)', 'admin_strategy_detail'),
    url(r'^admin/strategy_search/$', 'admin_strategy_search'),
    url(r'^admin/strategy_del/$', 'admin_strategy_del'),
)

urlpatterns += patterns('quant_data.views',
    url(r'stock/history_data$', 'stock_data_all'),
    url(r'stock/history_data_detail$', 'stock_detail_basic'))
# urlpatterns = patterns(r'^register/', register)
