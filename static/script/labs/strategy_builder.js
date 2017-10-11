String.prototype.isZh = function() {
    return this > '\u4e00' && this < '\u9fbb';
}
const buildervm = new Vue({
    el: '.strategy-builder',
    computed: {
        cashRemain() {
            const used = this.selectedStocks
            .map(stock => stock.weight)
            .reduce((a, e) => a+e, 0);

            return (100 - used).toFixed(2);
        },
        content() {
            return `#-*- coding:utf-8 -*-
import numpy as np

from zipline.api import order

# 第一步：设置基本参数
start = '${ this.startDate }'
end   = '${ this.endDate }'
capital_base = ${ this.capitalBase }
refresh_rate = ${ this.refreshRate }
benchmark = 'HS300'
freq = 'd'

# 第二步：选择主题，设置股票池
universes = [${ this.selectedStocks.map(stock => "'" + stock.code + "'").join(', ') }]

def initialize(context):
    # 第三步：调整股票权重，权重列表序号与股票池列表序号对应
    context.weight = [${ this.selectedStocks.map(stock => stock.weight/100.0).join(', ') }]
    context.weightmap = dict(zip(universes, context.weight))
    context.valid_secpos = dict(zip(universes, [0] * len(universes)))

def handle_data(context, data):
    # 本策略将使用context的以下属性：
    # context.portfolio.cash 表示根据前收计算的当前持有证券市场价值与现金之和。
    # data[<code>]['pirce'] 表示股票的参考价，一般使用的是上一日收盘价。
    # account.valid_secpos字典，键为证券代码，值为虚拟账户中当前所持有该股票的数量。

    # 本策略使用context以下属性
    #

    c = context.capital_base

    # 计算调仓数量
    change = {}
    for stock in universes:
        w = context.weightmap.get(stock, 0)
        p = data[stock]['price']
        if not np.isnan(p):
            change[stock] = int(c * w / p) - context.valid_secpos.get(stock, 0)
            context.valid_secpos[stock] = change[stock]

    # 按先卖后买的顺序发出指令
    for stock in sorted(change, key=change.get):
        order(stock, change[stock])`;
        }
    },
    methods: {
        reset() {
            this.$data = {
                startDate: (new Date()).getFullYear() - 1 + '-01-01',
                endDate: (new Date()).getFullYear() + '-01-01',
                capitalBase: 1000000,
                refreshRate: 5,
                step: 1,
                selectedStocks: [],
                candidateStocks: []
            }
            this.renderEditor();
        },
        select(stockName) {
            const stock = this.candidateStocks.filter(stock => stock.name === stockName)[0];
            if(stock) {
                if(this.selectedStocks.map(s => s.name).indexOf(stockName) === -1) {
                    this.selectedStocks.push({name: stock.name, code: stock.code, weight: 0});
                }
            }
            this.stockInput = '';
            this.renderEditor();
        },
        fetchCandidates() {
            const prefix = this.stockInput;
            if(!prefix) return;

            $.post(
                '/editor/stock_complete',
                { prefix: prefix, limit: 10},
                candidates => {
                    this.candidateStocks = candidates.map(item => {
                        return prefix.isZh()
                            ? { name: item.value, code: item.meta }
                            : { name: item.meta, code: item.value };
                    });
                    document.querySelector('.ui-autocomplete').style.display='';
                },
                'json'
            );
        },
        hideHintlist() {
            document.querySelector('.ui-autocomplete').style.display='none';
        },
        renderEditor() {
            const editor = ace.edit("editor");
            editor.setValue(this.content, -1);
        },
        validate() {
            var validate = true;
            if(!this.strategyName) {
                document.getElementById('strategy-name').classList.add('has-error');
                validate = false;
            } else {
                document.getElementById('strategy-name').classList.remove('has-error');
            }
            if(!this.startDate) {
                document.getElementById('start-date').classList.add('has-error');
                validate = false;
            } else {
                document.getElementById('start-date').classList.remove('has-error');
            }
            if(!this.endDate) {
                document.getElementById('end-date').classList.add('has-error');
                validate = false;
            } else {
                document.getElementById('end-date').classList.remove('has-error');
            }
            if(!this.capitalBase) {
                document.getElementById('capital-base').classList.add('has-error');
                validate = false;
            } else {
                document.getElementById('capital-base').classList.remove('has-error');
            }
            if(!this.refreshRate) {
                document.getElementById('refresh-rate').classList.add('has-error');
                validate = false;
            } else {
                document.getElementById('refresh-rate').classList.remove('has-error');
            }
            if (!validate) {
                this.step = 1;
            }
            return validate;
        },
        build() {
            if (!this.validate()) return;
            $.post(
                '/strategy/template/new/',
                {
                    name: this.strategyName,
                    start: this.startDate,
                    end: this.endDate,
                    capital_base: this.capitalBase,
                    freq: 'daily',
                    code: this.content
                },
                msg => {
                    if(msg.status == 'ok') {
                        $('#gen_strategy_modal').modal('hide');
                        this.reset();
                        location.reload();
                    } else {
                        console.error(msg.data);
                    }
                },
                'json'
            );
        }
    }
});

(() => {
    const editor = ace.edit("editor");
    editor.getSession().setMode("ace/mode/python");
    editor.setShowPrintMargin(false);
    editor.setReadOnly(true);
    editor.setHighlightActiveLine(false);
    buildervm.reset();
})();
