$(document).ready(function () {
    $('#search-button').click(function () {
        var query = $('#search-input').val();
        if (query.trim().length > 0) {
            search(query);
        }
    });

    function search(query) {
        $.ajax({
            type: 'GET',
            url: '/search-ajax/',  // Replace with your Django URL endpoint for search
            data: { query: query },
            success: function (response) {
                displayResults(response);
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    }
    function displayResults(results) {
        var tbody = $('#myTable tbody');
        tbody.empty();

        if (results.length > 0) {
            results.forEach(function (result) {
                var row = $('<tr>');
                $('<td>').text(result.faculty_Lname).appendTo(row);  // Last Name
                $('<td>').text(result.faculty_Fname).appendTo(row);  // First Name
                $('<td>').text(result.faculty_Mname).appendTo(row);  // Middle Name
                $('<td>').text(result.faculty_rank).appendTo(row);   // Rank
                $('<td>').text(result.semester).appendTo(row);        // Semester
                $('<td>').text(result.subject_code).appendTo(row);    // Subject Code
                $('<td>').text(result.total_average).appendTo(row);   // Total Average
                $('<td>').text(result.year).appendTo(row);            // Year
                $('<td>').text(result.student_name).appendTo(row);    // Evaluator
                // // Edit button
                // var editLink = $('<a>').attr('href', '{% url "edit_evaluation" evaluation.pk %}');
                // editLink.text('Edit');
                // $('<td>').append(editLink).appendTo(row);

                // // Delete button
                // var deleteForm = $('<form>').attr('method', 'post').attr('action', '{% url "delete_evaluation" evaluation.pk %}').attr('id', 'delete-form');
                // $('<input>').attr('type', 'hidden').attr('name', 'csrfmiddlewaretoken').val('{{ csrf_token }}').appendTo(deleteForm);
                // var deleteButton = $('<input>').attr('type', 'button').val('Delete').click(showConfirm);
                // deleteButton.appendTo(deleteForm);
                // $('<td>').append(deleteForm).appendTo(row);
                row.appendTo(tbody);
            });
        } else {
            var emptyRow = $('<tr>');
            $('<td colspan="9">').text('No results found.').appendTo(emptyRow);
            emptyRow.appendTo(tbody);
        }
    }
});
