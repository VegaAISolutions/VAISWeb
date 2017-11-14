var config = {
    countdown: {
        year: 2017,
        month: 12,
        day: 21,
        hour: 12,
        minute: 00,
        second: 00
    },

    subscription_form_tooltips: {
        success: 'You have been subscribed!',
        already_subscribed: 'You are already subscribed',
        empty_email: 'Please, Enter your email',
        invalid_email: 'Email is invalid. Enter valid email address',
        default_error: 'Error! Contact administration'
    }
}


$('#countdown').countdown('2018/01/01', function(event) {
$(this).html(event.strftime('%w weeks %d days %H:%M:%S'));
});
