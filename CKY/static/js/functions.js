function execute() {
    var data = {
        rules: $('#rules').val(),
        sentence: $('#sentence').val()
    }
    $.ajax({
        url: '/execute',
        data: data,
        type: 'POST',
        success: function (response) {
            console.log(JSON.parse(response));
            var result = JSON.parse(response);
            var html = "";
            $.each(result, function (rowNumber, rowData) {
                html += "<tr>";
                $.each(rowData, function (columnNumber, columnData) {
                    html += "<td>"; 
                    $.each(columnData, function (columnNumber, c) {
                        html += "<b>" + c.grammar + "</b>"
                        if (c.pos != '')
                            html += "<br/>" + "<small>" + c.pos + "</small>" + "<br/>"
                    });
                    html += "</td>";
                });
                html += "</tr>";
            });
            $("#myTable").html(html);
        },
        error: function (error) {
            console.log("Có lỗi xảy ra");
        }
    });

}
