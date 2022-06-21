$(function() {
    document.addEventListener('click', (e) => {
        let element = e.target;
        if(element.tagName == "BUTTON" && element.name=="payButton"){
            $.ajax({
                type: "POST",
                url: "/paid",
                data: JSON.stringify({'bill' : element.id}),
                contentType: "application/json",
                dataType: 'json',
                success: function(result) {
                    console.log(result)
                    if (result['processed']==true || result['processed']=='true') {
                        $("#notEnoughBalance").remove()
                        var i = 0
                        var temp
                        while (true) {
                            if (document.getElementsByClassName("status")[i].id == element.id) {
                                temp = document.getElementsByClassName("status")[i] 
                                break
                            }
                            i++
                        }
                        
                        console.log(temp)
                        $(temp).empty()
                        $(temp).append("Status: Completed")
                        $("#balance").empty()
                        $("#balance").append("Balance: ", result.balance.toString(10), "£")
                    }
                    else if (result['processed']==false || result['processed']=='false' ) {
                       $("#balance").empty()
                       $("#balance").append("Balance: ", result.balance.toString(10), "£")
                       $(".bills1").append('<h3 style="color:red" id="notEnoughBalance">Not Enough Balance</h3>') 
                    }
                } 
            });   
        }
        else if (element.tagName == "BUTTON" && element.id == "addBill") {
            $(".add").empty()
            $(".add").append('<form action="/Bills" class="forms" method="post" style="display: grid; grid-template-rows: 40px 40px 20px; grid-template-columns: 200px 200px" enctype="multipart/form-data">'+
                            '<label><input name = "name" placeholder= "Name" width="140px"></label>'+
                            '<label><input name = "amount" placeholder= "Amount" width="140px"></label>'+
                            '<label><input type="date" name="deadline" width="140px">Deadline</label>'+
                            '<input type = "file" name = "file">'+
                            '<button type="submit">Add</button></form>')
        }
        else if (element.tagName == "BUTTON" && element.id=="topUp") {
            $("#topUp").remove()
            $("#notEnoughBalance").remove()
            $(".bills1").append('<div style="display: grid; grid-template-row: 30px 25px"><label><input placeholder= "Amount" width="140px" id="topUpAmount" style="grid-row: 2; grid-column: 1"></label>'+
                                '<button type="button" style="width:40px; height:20px" id="topUpButton">Add</button></div>')
        }
        else if(element.tagName == "BUTTON" && element.id=="topUpButton") {
            var input = document.getElementById("topUpAmount").value
            if (input == null || input == '') {
                $(".bills1").append('<p style="color: red" id="error">Input data</p>')
            }
            else {
            $("#error").remove()
            $.ajax({
                type: "POST",
                url: "/topUp",
                data: JSON.stringify({'amount' : input}),
                contentType: "application/json",
                dataType: 'json',
                success: function(result) {
                    $("#balance").empty()
                    $("#balance").append("Balance: ", result.balance.toString(10), "£")
                    $("#topUpAmount").remove()
                    $("#topUpButton").remove()
                    $(".bills1").append('<button type="button" id="topUp" style="width: 100px; height: 30px">Top Up</button>')
                }
            });
        }
        }
        if(element.tagName == "BUTTON" && element.name=="removeButton"){
            $.ajax({
                type: "POST",
                url: "/paid",
                data: JSON.stringify({'bill' : element.id}),
                contentType: "application/json",
                dataType: 'json',
                success: function(result) {
                    console.log(result)
                    var temp = document.getElementsByName(element.id)[0]
                    temp.remove()
                }
            })
        }
    })
}) 
    