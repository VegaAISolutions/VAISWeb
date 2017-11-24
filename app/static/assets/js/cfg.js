
$('#countdown').countdown('2017/12/17', function(event) {
$(this).html(event.strftime('%w Weeks %d Days %H:%M:%S'));
});

/*$.getScript('/static/assets/js/jquery.flot.js',function(){
$.getScript('/static/assets/js/jquery.flot.pie.js',function(){


var data = [],
			series = Math.floor(Math.random() * 6) + 3;

		for (var i = 0; i < series; i++) {
			data[i] = {
				label: "Series" + (i + 1),
				data: Math.floor(Math.random() * 100) + 1
			}
		}


$.plot('#p1', data, {
    series: {
        pie: {
            show: true
        }
    }
});
$.plot('#p2', data, {
    series: {
        pie: {
            innerRadius: 0.5,
            show: true
        }
    }
});
$.plot('#p3', data, {
    series: {
        pie: {
            innerRadius: 0.5,
            show: true
        }
    }
});
})});*/

$(document).ready(function () {
        $('.collapse.in').prev('.panel-heading').addClass('active');
        $('#accordion, #bs-collapse')
            .on('show.bs.collapse', function (a) {
                $(a.target).prev('.panel-heading').addClass('active');
            })
            .on('hide.bs.collapse', function (a) {
                $(a.target).prev('.panel-heading').removeClass('active');
            });
    });