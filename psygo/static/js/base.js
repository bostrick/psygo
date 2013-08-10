
function TableManager(form) {

    this.form = form;
    this.element = $(form);
    this.table = this.element.find("table.dataTable");
    this.action = this.form.action;

    this.reinit_table();
    
}

function tm_make_target_link(data, type, obj) {
    console.log(data);
    console.log(obj);
    var s  = '<a href="' + obj.uuid + '">' + data + '</a>';
    console.log(s);
    return s;
}


TableManager.prototype.reinit_table = function () {

    console.log("reinit table")
    $.ajax({
        'context': this,
        'url': this.action,
    }).done(this.init_table_cb);

}
        

TableManager.prototype.init_table_cb = function (data) {

    console.log("init_table_cb");
    console.log(this);
    console.log(data);

    if ( $.fn.DataTable.fnIsDataTable(this.table) ) {
        console.log("out with the old");
        this.table.fnDestroy();
    }
    this.table.dataTable(data);
}
