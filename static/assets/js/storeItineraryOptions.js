/*! jQuery v1.11.1 | (c) 2005, 2014 jQuery Foundation, Inc. | jquery.org/license */
function storeItineraryOptions() {
    var x = document.getElementById("Input_Fields");
    var city =  String(x.elements[0].value);
    var budget = String(x.elements[1].value);
    var itineraryOptions = '{ "city" : "' + city + '" , "budget" : "' + budget + '" }';
	itineraryOptionsJSON = JSON.parse(itineraryOptions);
	//Erase this line for the future! it just prints 
	//document.getElementById("demo").innerHTML =itineraryOptionsJSON.city + " " + itineraryOptionsJSON.budget;

	window.location = 'results.html';
}



(function($){
	var initLayout = function() {
		var hash = window.location.hash.replace('#', '');
		var currentTab = $('ul.navigationTabs a')
							.bind('click', showTab)
							.filter('a[rel=' + hash + ']');
		if (currentTab.size() == 0) {
			currentTab = $('ul.navigationTabs a:first');
		}
		showTab.apply(currentTab.get(0));
		
		$('.inputDate').DatePicker({
			format:'m/d/Y',
			date: $('#inputDate').val(),
			current: $('#inputDate').val(),
			starts: 1,
			position: 'right',
			onBeforeShow: function(){
				$('#inputDate').DatePickerSetDate($('#inputDate').val(), true);
			},
			onChange: function(formated, dates){
				$('#inputDate').val(formated);
				$('#inputDate').DatePickerHide();
				var selectedDate = $('#inputDate').DatePickerGetDate();
				document.getElementById("demo22").innerHTML = selectedDate;
			}
		});
		var now3 = new Date();
		now3.addDays(-4);
		var now4 = new Date()
		
		$('#widgetCalendar div.datepicker').css('position', 'absolute');
	};
	
	var showTab = function(e) {
		var tabIndex = $('ul.navigationTabs a')
							.removeClass('active')
							.index(this);
		$(this)
			.addClass('active')
			.blur();
		$('div.tab')
			.hide()
				.eq(tabIndex)
				.show();
	};
	
	EYE.register(initLayout, 'init');
})(jQuery)