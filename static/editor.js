$( document ).ready(function() {

    var curr_data;
    var timeoutId;
    $('form input, form textarea').on('input propertychange change', function() {
        
        clearTimeout(timeoutId);
        timeoutId = setTimeout(function() {
            // Runs 1 second (1000 ms) after the last change    
            saveToDB();
        }, 1000);
    });

    function saveToDB()
    {
        curr_data = document.getElementById("journal-entry").value
        // Now show them we saved and when we did
        var d = new Date();
        $('#last-saved').html('Saved! Last: ' + d.toLocaleTimeString());

        // Post data to Python
        $.post( "/save", {
            curr_text: curr_data 
        });
    }

})