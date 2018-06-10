(function($,window){
    var roleAdd = {
        //初始化
        init: function(){
            //操作权限 
            var setpermission = {
                async : {
                    url : "role/choicePermissionTree",
                    type : "post",
                    enable : true,
                    autoParam : [ "id" ],
                    dataType : "json",
                },
                check : {
                    enable : true,
                    chkStyle : "checkbox",
                    chkboxType : {
                        "Y" : "ps",
                        "N" : "ps"
                    }, 
                    radioType : "all"
                },
                view : {
                    dblClickExpand : false
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    beforeClick : roleAdd.beforeClickPermission,
                    beforeCheck: roleAdd.zTreeBeforeCheck,
                    onCheck : roleAdd.onCheckPermission
                }
            }
            $.fn.zTree.init($("#permissionDemo"), setpermission, null);
            $(".modal-body").addClass("modal-body-overflow");
        },
        zTreeBeforeCheck: function(treeId, treeNode){
        	var flag;
        	var zTree = $.fn.zTree.getZTreeObj("permissionDemo");
        	if(treeNode.isParent){
        		flag = true;
        	}else{
        		flag = false;
        		zTree.checkNode(treeNode, !treeNode.checked, !treeNode.checked);
        	};
        	return flag;
        },
        beforeClickPermission: function(treeId, treeNode){
            var zTree = $.fn.zTree.getZTreeObj("permissionDemo");
            zTree.checkNode(treeNode, !treeNode.checked, true, true);
            return false;
        },
        onCheckPermission: function(e, treeId, treeNode){
        	if(!treeNode.isParent){
        		return false;
        	};
            var zTree = $.fn.zTree.getZTreeObj("permissionDemo");
            var nodes = zTree.getCheckedNodes(true);
            var v = "";
            for (var i = 0, l = nodes.length; i < l; i++) {
                v += nodes[i].name + ",";
            };
        },
        //提交
        doSubmit: function(){
            var list = [];
            var editlist = [];
            var checkNodes = $.fn.zTree.getZTreeObj("permissionDemo").getCheckedNodes(true);
            if (checkNodes != null && checkNodes.length > 0) {
                for (var i = 0; i < checkNodes.length; i++) {
                    var obj = {};
                    if (checkNodes[i].type == "premissionEdit") { // 可写 
                        editlist.push(checkNodes[i].pId); 
                    }else{
                        obj.id = checkNodes[i].id;
                        obj.edit = false;
                        list.push(obj);
                    }
                }
            }
            // 重组可写的权限 
            if (list.length > 0 && editlist.length >0) {
                for (var i = 0; i < list.length; i++) {
                    for (var j =0; j< editlist.length; j++) {
                        if (list[i].id == editlist[j]) {
                            list[i].edit = true;
                        }
                    }
                }
            }
            $("#permissionTree").val(JSON.stringify(list));
            if(roleAdd.validates()){
                $("#addForm").ajaxSubmit(function(data) {
                    console.log(data);
                    if (data != null) {
                        var result = $.parseJSON(data);
                        if (result.success) {
                            console.log(result.success,result.obj.flag)
                            if (result.obj.flag == 1){
                                $("#commonSmWin").modal("hide");
                                layer.msg("添加成功！",{move:false});
                                myTable.requestData();
                            }else{
                                layer.msg(result.obj.errMsg,{move:false});
                            }
                        }else{
                            layer.msg(result.msg,{move:false});
                        }
                    }
                });
            }
        },
        //校验
        validates: function(){
            return $("#addForm").validate({
                rules : {
                    name : {
                        required : true,
                        maxlength : 20
                    },
                    notes : {
                        maxlength : 140
                    }
                },
                messages : {
                    name : {
                        required : roleNameNull,
                        maxlength : publicSize20
                    },
                    notes : {
                        maxlength : publicSize140
                    }
                }
            }).form();
        },
    }
    $(function(){
        roleAdd.init();
        $('input').inputClear();

        //优先级策略单选组选择
        $(".priority-group").on("click","input",function () {
            $(".priority-group input").prop("checked",false);
            $(this).prop("checked",true)
        });
        
        $("#doSubmitAdd").on("click",roleAdd.doSubmit);
    })
})($,window)
