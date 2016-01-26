/*

Command to run it:
    mongo REPLACEME_DBNAME --eval "pipeline='sales_by_product';" aggregation.js

    Typically, you should see something like this if the mapreduce ran correctly.

    MongoDB shell version: 2.4.8
    connecting to: storycs
    2013-12-20 00:00:00
    {
        "result" : "YOUR COLLECTION NAME",
        "timeMillis" : 11,
        "counts" : {
            "input" : 4,
            "emit" : 4,
            "reduce" : 2,
            "output" : 2
        },
        "ok" : 1,
    }

    You can run the mongo interpreter and check that the
    collection sales_by_product is created by this pipeline.

*/

var pipeline;

function main() {
    if (pipeline == 'sales_by_product') {
        printjson(db.sales.mapReduce(
                mapSalesByProduct,
                reduceSalesByProduct,
                {
                        out: {merge: "sales_by_product"},
                        query: {},  // adjust on timestamp of sale, etc
                        scope: {}  // pass in extra functions here
                }));
    }
}


/* -----------------------------------------------------------------
                   Pipeline 'Sales By Product'
----------------------------------------------------------------- */
// We want to know how many sales were made in total, by product.
// We map with key on the product_id and in reduce we simply count the quantities.


var mapSalesByProduct = function() {
    // Input: Sale
    // Output: {product_id: quantity}
    for (var i_product_sale in this.products) {
        var product_sale = this.products[i_product_sale]; 
        emit({product_id: product_sale.product_id},
             {count: product_sale.quantity});
    }
};


var reduceSalesByProduct = function(unused_key, objs) {
    // objs : [{count:}].
    // We just do regular counts.
    var ret = {count: 0};
    for (var i = 0; i < objs.length; i++) {
        var o = objs[i];
        ret.count += o.count;
    }
    return ret;
};


main();