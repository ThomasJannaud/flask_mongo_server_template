/*
Defines the data aggregation pipeline on mongodb.

_ Collections
 -'raw_...' contains documents of the form {, ...}.

_ Pipelines
  -'xxx': (to be computed hourly or daily)
    yyyyyyyy

    In: raw_...
    Global variables :
        pipeline: 'xxx'
        start_timestamp: 1389600000. Default: last rounded time period with regard to cron_type. (yesterday if daily, ...)
        end_timestamp: same format and default, coupled with start_timestamp.
    Out: out_xxxx


Command to run it:
    mongo testdb --eval "pipeline=...; glob_var_1=...; glob_var_2=...; ..." aggregation.js

    Typically, you should see something like this if the mapreduce ran correctly.

    MongoDB shell version: 2.4.8
    connecting to: storycs
    2013-12-20 00:00:00
    {
        "result" : "out_by_app_day",
        "timeMillis" : 11,
        "counts" : {
            "input" : 4,
            "emit" : 4,
            "reduce" : 2,
            "output" : 2
        },
        "ok" : 1,
    }


Implementation details:
    _ All timestamps are in seconds.

*/


var start_timestamp, end_timestamp;
var pipeline;

function main() {
    // Parses command line arguments (global variables) and launches the right pipeline appropriately.
    var NUM_SEC_PER_HOUR = 3600;
    var NUM_SEC_PER_DAY = 24 * NUM_SEC_PER_HOUR;
    if (pipeline == 'by_app_aggregate') {
        if (start_timestamp === undefined) {
            end_timestamp = GetByAppAggregateKeyTimestamp(GetCurrentTimestamp());
            if (aggregate_time_interval == 'hour') {
                start_timestamp = end_timestamp - NUM_SEC_PER_HOUR;
                end_timestamp += NUM_SEC_PER_HOUR;
            } else if (aggregate_time_interval == 'day') {
                start_timestamp = end_timestamp - NUM_SEC_PER_DAY;
                end_timestamp += NUM_SEC_PER_DAY;
            }
        }
        printjson(db.raw_bt_events_historic.mapReduce(
                mapByApp,
                reduceByApp,
                {
                        out: {merge: "out_by_app_" + aggregate_time_interval},
                        query: {"timestamp": {$gte: start_timestamp, $lt: end_timestamp}},
                        scope: {aggregate_time_interval: aggregate_time_interval,
                                        GetByAppAggregateKeyTimestamp: GetByAppAggregateKeyTimestamp}
                }));
    }
}


/* -----------------------------------------------------------------
                   Pipeline 'xxx'
----------------------------------------------------------------- */
// We want to have some basic stats on all the logs by app on period of times (daily, hourly, ...)
// We map by app and by timestamp (beginning of the period) all the values, in reduce we count them


var mapByApp = function() {
    var timestamp = GetByAppAggregateKeyTimestamp(this.timestamp);
    emit({app_id: this.app_id, timestamp: timestamp},
             {count_in: (this.geofencing_type == 0 ? 1 : 0),
                count_out: (this.geofencing_type == 1 ? 1 : 0)});
};


var reduceByApp = function(unused_key, objs) {
    // objs : [{count_in:, count_out:, ...}].
    // We just do regular counts.
    var ret = {count_in: 0, count_out: 0};
    for (var i = 0; i < objs.length; i++) {
        var o = objs[i];
        ret.count_in += o.count_in;
        ret.count_out += o.count_out;
    }
    return ret;
};


/* -----------------------------------------------------------------
                             Utils
----------------------------------------------------------------- */
function GetCurrentTimestamp() {
    var NUM_MILLIS_PER_SEC = 1000;
    return NumberLong(new Date().getTime() / NUM_MILLIS_PER_SEC);
}


function dynamicSort(property) {
    // my_array.sort(dynamicSort("[-]var")) will sort my_array's objects with regard to object.var
    // ascendingly or descendingly if there is the '-'.
    var sortOrder = 1;
    if (property[0] === "-") {
            sortOrder = -1;
            property = property.substr(1);
    }
    return function (a,b) {
            var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
            return result * sortOrder;
    }
}


main();