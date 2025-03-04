$(document).ready(function() {
    $('#callApiButton').click(function() {
        $.ajax({
            url: '/api/hello',
            type: 'GET',
            success: function(data) {
                $('#result').text(data.message);
            },
            error: function() {
                $('#result').text('Error calling API');
            }
        });
    });

    $('#callSwaggerButton').click(function() {
        $.ajax({
            url: '/swagger',
            type: 'GET',
            success: function(data) {
                $('#result').text(data.message);
            },
            error: function() {
                $('#result').text('Error calling API');
            }
        });
    });
});
