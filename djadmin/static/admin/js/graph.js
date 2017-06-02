/**
 * Created by Neeraj Kumar on 5/18/2017.
 */
var randomColorGenerator = function () {
    return '#' + (Math.random().toString(16) + '0000000').slice(2, 8);
};
var options_data = {
    responsive: true,
    legend: {
        display:false
    },
    title: {
        display: true,
    },
    animation: {
        animateScale: true,
        animateRotate: true
    },
    tooltips: {
        callbacks: {
            label: function (tooltipItem, data) {
                var allData = data.datasets[tooltipItem.datasetIndex].data;
                var _meta = data.datasets[tooltipItem.datasetIndex]._meta;
                var meta = _meta[Object.keys(_meta)[0]];
                var tooltipLabel = data.labels[tooltipItem.index];
                var tooltipData = allData[tooltipItem.index];
                var tooltipPercentage = Math.round((tooltipData / meta.total) * 10000) / 100;
                return tooltipLabel + ': ' + tooltipData + ' (' + tooltipPercentage + '%)';
            }
        }
    }
};
