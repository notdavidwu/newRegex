
    scrolling1=false
    scrolling2=false
    scrolling3=false
    scrolling4=false

    function test() {
        $('#CT-PET').css('margin-top','50px')
        $('#CT-PET').css('width',$(window).width()*0.7)
        $('#CT-PET').css('height',0)
        $("#frame1").children("label").children('div').children('div').children('img').css('display','none');
        $("#frame2").children("label").children('div').children('div').children('img').css('display','none');
        $("#frame3").children("label").children('div').children('div').children('img').css('display','none');
        $("#frame4").children("label").children('div').children('div').children('img').css('display','none');
        $('.slider').css('display','none')
        $('.loader').css('display','inline')
        $('.loader').css('top',$(window).height()/2)
        $('#Topcheckbox').prop('chencked',false)
        $('#Topcheckbox').prop('disabled',true)
    }
    a=0

    function connect(window_sno){
        let height=Math.floor($('#frame'+window_sno).children('label').children('.slider').height());
        let b = $('#frame'+window_sno).children('label').children('.slider').scrollTop();
        let num = Math.floor($('#frame'+window_sno).children('label').children('.slider').children().height()/height)
        count1=Math.floor(b/height)

        plane=$("#frame"+window_sno).children('label').children('div').children('div').children('.plane').text()
        $("#frame"+window_sno).children('label').children('div').children('div').children('.variable').text(count1+1+'/'+num)
        //if($('#frame1').children('input').is(':checked')){
        if(plane=='Axial'){
            $('#frame'+window_sno).children('label').children('div').children('div').children('.z').text(count1);
        }else if(plane=='Coronal'){
            $("#frame"+window_sno).children('label').children('div').children('div').children('.y').text(count1);
        }else if(plane=='Sagittal'){
            $("#frame"+window_sno).children('label').children('div').children('div').children('.x').text(count1);
        }
        //}
        
        let x=$('#frame'+window_sno).children('label').children('div').children('div').children('.x').text()
        let y=$('#frame'+window_sno).children('label').children('div').children('div').children('.y').text()
        let z=$("#frame"+window_sno).children('label').children('div').children('div').children('.z').text();

        frameXYZ=checkPlaneXYZ(plane,x,y,count1)

        win_num=$('#select').val()
        let imageType = $('#frame'+window_sno).children('label').children('div').children('div').children('.StudyDes').text()
        if(imageType!='MRI'){
            var Con=[]
            for(var i =0;i<win_num;i++) {
                Con.push($('.StudyDes').eq(i).text()+'_'+$('.StudyID').eq(i).text()+'_'+$('.StudyDate').eq(i).text()+'_'+$('.SeriesID').eq(i).text())
            }
            for(var i =0;i<win_num;i++) {
                if(Con[i]==Con[window_sno-1]){
                    var ind=i+1
                    if(ind!=window_sno){
                        comparePlane = $('#frame'+ind).children('label').children('div').children('div').children('.plane').text()
                        if(plane==comparePlane){
                            $("#frame"+ind).children('label').children('.slider').scrollTop(frameXYZ['z']*$("#frame"+ind).children('label').children('.slider').height())
                            
                            let height = Math.floor($('#frame'+ind).children('label').children('.slider').height());
                            let b = $('#frame'+ind).children('label').children('.slider').scrollTop();
                            let num = Math.floor($('#frame'+ind).children('label').children('.slider').children().height()/height)
                            let count=Math.floor(b/height)
                            $('#frame'+ind).children('label').children('div').children('div').children('.variable').text(count+1+'/'+num)
                        }
                        if(plane=='Axial'){
                            $('#frame'+ind).children('label').children('div').children('div').children('.z').text(count1)
                        }else if(plane=='Coronal'){
                            $('#frame'+ind).children('label').children('div').children('div').children('.y').text(count1)
                        }else if(plane=='Sagittal'){
                            $('#frame'+ind).children('label').children('div').children('div').children('.x').text(count1)
                        }
                    }
                    ajax_connect_view(ind)
                    //ajax(ind,frameXYZ['x'],frameXYZ['y'],frameXYZ['z'],true,true)
                }
            }
        }else{
            var Con=[]
            for(var i =0;i<win_num;i++) {
                Con.push($('.StudyDes').eq(i).text()+'_'+$('.StudyID').eq(i).text()+'_'+$('.StudyDate').eq(i).text()+'_'+$('.SeriesID').eq(i).text()[1])
            }
            for(var i =0;i<win_num;i++) {
                if(Con[i]==Con[window_sno-1]){
                    var ind=i+1
                    if(ind!=window_sno){
                        if($('.SeriesID').eq(i).text()[0]==$('.SeriesID').eq(window_sno-1).text()[0]){
                            $("#frame"+ind).children('label').children('.slider').scrollTop(frameXYZ['z']*$("#frame"+ind).children('label').children('.slider').height())
                            
                            let height = Math.floor($('#frame'+ind).children('label').children('.slider').height());
                            let b = $('#frame'+ind).children('label').children('.slider').scrollTop();
                            let num = Math.floor($('#frame'+ind).children('label').children('.slider').children().height()/height)
                            let count=Math.floor(b/height)
                            $('#frame'+ind).children('label').children('div').children('div').children('.variable').text(count+1+'/'+num)
                            $('#frame'+ind).children('label').children('div').children('div').children('.z').text(count1)
                        }
                    }
                    ajax_connect_view(ind)
                    //ajax(ind,frameXYZ['x'],frameXYZ['y'],frameXYZ['z'],true,true)

                }
            }
        }
    }
    function ajax1(event){
        if(scrolling1==true){
            connect(1)
        }

    }(jQuery);
    
    function ajax2(event){
        if(scrolling2==true){
            connect(2)
        }
    }(jQuery);
    function ajax3(event){
        if(scrolling3==true){
            connect(3)
        }
    }(jQuery);
    function ajax4(event){
        if(scrolling4==true){
            connect(4)
        }
    }(jQuery);


    $(document).on("pagecreate","#pageone",function(){
        $("#frame1").on("swipe",function(){

        });                       
      });

    function myFunction(event) {
        document.getElementById("frame1").onmousewheel = function(e){
            let height=$('#frame1').children('label').children('.slider').height();
            let b = $('#frame1').children('label').children('.slider').scrollTop();
            let count=Math.round(b/height);
            /*滑鼠滾動的量 下滾是負 上滾是正*/
            if(e.wheelDelta < 0){
                count ++;
            }else{
                count --;
            }
            let z = Math.round($('#frame1').children('label').children('.slider').children('div').height()/height)
            if (count < 0){
                count = 0
            }else if (count >= z-1) {
                count = z-1
            }
            b = count*height
            $('#frame1').children('label').children('.slider').scrollTop(b);
            scrolling1=true
            scrolling2=false
            scrolling3=false
            scrolling4=false
        }
        document.getElementById("frame2").onmousewheel = function(e){

            let height=$('#frame2').children('label').children('.slider').height();
            let b = $('#frame2').children('label').children('.slider').scrollTop();
            let count=Math.round(b/height);
            if(e.wheelDelta < 0){
                count ++;
            }else{
                count --;
            }
            let z = Math.round($('#frame2').children('label').children('.slider').children('div').height()/height)
            if (count < 0){
                count = 0
            }else if (count >= z-1) {
                count = z-1
            }
            b = count*height
            $('#frame2').children('label').children('.slider').scrollTop(b);
            scrolling1=false
            scrolling2=true
            scrolling3=false
            scrolling4=false
        }
        document.getElementById("frame3").onmousewheel = function(e){

            let height=$('#frame3').children('label').children('.slider').height();
            let b = $('#frame3').children('label').children('.slider').scrollTop();
            let count=Math.round(b/height);
            if(e.wheelDelta < 0){
                count ++;
            }else{
                count --;
            }
            let z = Math.round($('#frame3').children('label').children('.slider').children('div').height()/height)
            if (count < 0){
                count = 0
            }else if (count >= z-1) {
                count = z-1
            }
            b = count*height
            $('#frame3').children('label').children('.slider').scrollTop(b);
            scrolling1=false
            scrolling2=false
            scrolling3=true
            scrolling4=false
        }
        document.getElementById("frame4").onmousewheel = function(e){

            let height=$('#frame4').children('label').children('.slider').height();
            let b = $('#frame4').children('label').children('.slider').scrollTop();
            let count=Math.round(b/height);
            if(e.wheelDelta < 0){
                count ++;
            }else{
                count --;
            }
            let z = Math.round($('#frame4').children('label').children('.slider').children('div').height()/height)
            if (count < 0){
                count = 0
            }else if (count >= z-1) {
                count = z-1
            }
            b = count*height
            $('#frame4').children('label').children('.slider').scrollTop(b);
            //document.getElementById('view1').scrollTop= b
            scrolling1=false
            scrolling2=false
            scrolling3=false
            scrolling4=true
        }
    }(jQuery);
    function bb(){
        $(".slider").prev(".main").children('div').children('p').text()
    }
    function mouseover(event){

        $('#CTWC').val($("[name='group1']:checked").next("label").children('div').children('div').children('.CTWC').text())
        $('#CTWW').val($("[name='group1']:checked").next("label").children('div').children('div').children('.CTWW').text())
        $('#PETWC').val($("[name='group1']:checked").next("label").children('div').children('div').children('.PETWC').text())
        $('#PETWW').val($("[name='group1']:checked").next("label").children('div').children('div').children('.PETWW').text())
        $('#MRIWC').val($("[name='group1']:checked").next("label").children('div').children('div').children('.MRIWC').text())
        $('#MRIWW').val($("[name='group1']:checked").next("label").children('div').children('div').children('.MRIWW').text())
        var Des = $("[name='group1']:checked").next("label").children('div').children('div').children('.StudyDes').text()
        
        var mode=$("[name='group1']:checked").next("label").children('div').children('div').children('.mode').text()
        $('#Mode_menu').val(mode).prop('selected',true);
        $('#Mode').val(mode).prop('selected',true);

        var CT_window=$("[name='group1']:checked").next("label").children('div').children('div').children('.CT_window').text()
        $('#CTWindow').val(CT_window).prop('selected',true);
        $('#CTWindow_menu').val(CT_window).prop('selected',true);
        var LocalMax = $("[name='group1']:checked").next("label").children('div').children('div').children('.LocalMax').text()
        var LocalMax_disable = $("[name='group1']:checked").next("label").children('div').children('div').children('.LocalMax_disable').text()
        if (LocalMax=='true'){
            $('#LocalMax').children('input').prop('checked',true);
        }else{
            $('#LocalMax').children('input').prop('checked',false);
        }
        if (LocalMax_disable=='true'){
            $('#LocalMax').children('input').prop('disabled',true);
        }else{
            $('#LocalMax').children('input').prop('disabled',false);
        }
        if(Des=='PET'){
            $('#viewPlane').prop('disabled',false);
            $('#Mode').prop('disabled',false);
            $('#CT_Group').css('display','inline-flex');
            $('#PET_Group').css('display','inline-flex');
            $('#MRI_Group').css('display','none');
            $('#CTWindow_menu').prop('disabled',false);
            $('#Mode_menu').prop('disabled',false);
            $('#Plane_menu').prop('disabled',false);
            $('#SaveCoordinate').css('display','none')
            $('#RT_Contour').css('display','none')
            $('#MRI_tool').css('display','none')
        }else if(Des=='MRI'){
            $('#viewPlane').prop('disabled',true);
            $('#Mode').prop('disabled',true);
            $('#CT_Group').css('display','none');
            $('#PET_Group').css('display','none');
            $('#MRI_Group').css('display','inline-flex');
            $('#CTWindow_menu').prop('disabled',true);
            $('#Mode_menu').prop('disabled',true);
            $('#Plane_menu').prop('disabled',true);
            $('#SaveCoordinate').css('display','inline-block')
            $('#MRI_tool').css('display','inline-block')
            
            $('#MRI_tool').css('background-color','rgba(255,255,255,0.7)')
            $('#RT_Contour').css('display','none')
        }else if(Des=='RTPLAN'){
            $('#viewPlane').prop('disabled',false);
            $('#Mode').prop('disabled',true);
            $('#RT_Contour').css('display','inline-block')
            
            $('#RT_Contour').css('background-color','rgba(255,255,255,0.7)')
            $('#CT_Group').css('display','inline-flex');
            $('#PET_Group').css('display','none');
            $('#MRI_Group').css('display','none');

            $('#CTWindow_menu').prop('disabled',false);
            $('#Mode_menu').prop('disabled',false);
            $('#Plane_menu').prop('disabled',false);
            $('#SaveCoordinate').css('display','none')
            $('#MRI_tool').css('display','none')
        }else{
            $('#viewPlane').prop('disabled',false);
            $('#Mode').prop('disabled',true);
            $('#CT_Group').css('display','inline-flex');
            $('#PET_Group').css('display','none');
            $('#MRI_Group').css('display','none');
            $('#CTWindow_menu').prop('disabled',false);
            $('#Mode_menu').prop('disabled',false);
            $('#Plane_menu').prop('disabled',false);
            $('#SaveCoordinate').css('display','none')
            $('#RT_Contour').css('display','none')
            $('#MRI_tool').css('display','none')
        }
        
        var plane=$("[name='group1']:checked").next("label").children('div').children('div').children('.plane').text()
        plane=plane.replace(/\s+/g, '')
        $('#viewPlane').val(plane).prop('selected',true);
        $('#Plane_menu').val(plane).prop('selected',true);

        var StudyDes = $("[name='group1']:checked").next("label").children('div').children('div').children('.StudyDes').text()
        //console.log($("[name='group1']:checked").next("label").children('div').children('div').children('.series').text())
        if(StudyDes=='RTPLAN'){
            $.ajax({
                type: 'post',
                url: "{% url 'DICOM:RT_change' %}", // this is the mapping between the url and view
                data: {
                    'WindowNo':$("[name='group1']:checked").next("label").children('div').children('div').children('.series').text(),
                    'csrfmiddlewaretoken': window.CSRF_TOKEN
                },
                success: function(response) {
                    $('#RT_Contour').empty()

                    for (var i = 0; i < response.ROIname.length; i++) {
                        if (response.index != -1) {
                            if (response.index.indexOf(i) != -1) {
                                
                                $('#RT_Contour').append('' +
                                '<div class="form-check form-switch">' +
                                '<input checked class="form-check-input" onchange="drawContour()" type="checkbox" name="RT" id="' + response.ROIname[i] + '">' +
                                '<label class="form-check-label" for="' + response.ROIname[i] + '">' + response.ROIname[i] + '</label>' +
                                '<div style="display:inline-block;position:absolute;right: 0px ;width:20px;height: 20px;background-color: rgb(' + response.color[i] + ')"></div>' +
                                '</div>' +
                                '')
                            } else {
                                $('#RT_Contour').append('' +
                                '<div class="form-check form-switch">' +
                                '<input class="form-check-input" onchange="drawContour()" type="checkbox" name="RT" id="' + response.ROIname[i] + '">' +
                                '<label class="form-check-label" for="' + response.ROIname[i] + '">' + response.ROIname[i] + '</label>' +
                                '<div style="display:inline-block;position:absolute;right: 0px ;width:20px;height: 20px;background-color: rgb(' + response.color[i] + ')"></div>' +
                                '</div>' +
                                '')
                            }
                        }else{
                            $('#RT_Contour').append('' +
                            '<div class="form-check form-switch">' +
                            '<input class="form-check-input" onchange="drawContour()" type="checkbox" name="RT" id="' + response.ROIname[i] + '">' +
                            '<label class="form-check-label" for="' + response.ROIname[i] + '">' + response.ROIname[i] + '</label>' +
                            '<div style="display:inline-block;position:absolute;right: 0px ;width:20px;height: 20px;background-color: rgb(' + response.color[i] + ')"></div>' +
                            '</div>' +
                            '')
                        }
                    }
                }
            });
        }else{
            $('#RT_Contour').empty()
        }
        if(win_num==1){
            $('#frame1').css('background-color','#33333a');
        }else{
            $("[name='group1']:checked").parents('div').css('background-image',
                'repeating-linear-gradient(to bottom, #FFFFFF 0,#FFFFFF 1%,transparent 1%, transparent 99%),' +
                'repeating-linear-gradient(to right, #FFFFFF 0,#FFFFFF 1%,#33333a 1%,#33333a 99%)'
            )

            $("[name='group1']:not(':checked')").parents('div').css('background','none');
            $("[name='group1']:not(':checked')").parents('div').css('background-color','#33333a');
        }

        var number=$("[name='group1']:checked").next("label").children('div').children('div').children('.series').text()

        if(number==1){
            scrolling1=true
            scrolling2=false
            scrolling3=false
            scrolling4=false
        }else if(number==2){
            scrolling1=false
            scrolling2=true
            scrolling3=false
            scrolling4=false
        }else if(number==3){
            scrolling1=false
            scrolling2=false
            scrolling3=true
            scrolling4=false
        }else if(number==4){
            scrolling1=false
            scrolling2=false
            scrolling3=false
            scrolling4=true
        }
        //let window_sno = $("[name='group1']:checked").next("label").children('div').children('div').children('.series').text()
        //functionAjax=[ajax1(),ajax2(),ajax3(),ajax4()]
        //functionAjax[window_sno]
    }
    function ajax_connect_view(name){
        var height=$('#frame'+name.toString()).children('label').children('.slider').height();
        var b = $('#frame'+name.toString()).children('label').children('.slider').scrollTop();
        var count=Math.round(b/height);
        var x=$('#frame'+name.toString()).children('label').children('div').children('#dicom'+name).children('.x').text()
        var y=$('#frame'+name.toString()).children('label').children('div').children('#dicom'+name).children('.y').text()
        var z=$('#frame'+name.toString()).children('label').children('div').children('#dicom'+name).children('.z').text()
        var plane=$("#frame"+name.toString()).children('label').children('div').children('div').children('.plane').text()
        var xyz=checkPlaneXYZ(plane,x,y,z)
        //alert($('#frame1').children('label').children('div').children('#dicom'+name).children('.z').text())
        ajax(name, xyz['x'], xyz['y'], xyz['z'],true, true)
    }
    //window.location.reload(true);
    
    function ajax(name,x,y,z,ActualCoordinates,drawActualCoordinates){
        if(name==1){
            urlname=urlname1
        }else if(name==2){
            urlname=urlname2
        }else if(name==3) {
            urlname=urlname3
        }else if(name==4){
            urlname=urlname4
        }
        //console.log(JSON.parse("[" + $("#frame"+name.toString()).children('label').children('div').children('div').children('.MRIWW').text() + "]")[z])
        StudyDes = $("#frame"+name.toString()).children('label').children('div').children('div').children('.StudyDes').text()
        if(StudyDes=='PET'){
            var WC = $("#frame"+name.toString()).children('label').children('div').children('div').children('.PETWC').text()
            var WW = $("#frame"+name.toString()).children('label').children('div').children('div').children('.PETWW').text()
        }else if(StudyDes=='RTPLAN'){
            var WC = $("#frame"+name.toString()).children('label').children('div').children('div').children('.CTWC').text()
            var WW = $("#frame"+name.toString()).children('label').children('div').children('div').children('.CTWW').text()
        }else if(StudyDes=='CT'){
            var WC = $("#frame"+name.toString()).children('label').children('div').children('div').children('.CTWC').text()
            var WW = $("#frame"+name.toString()).children('label').children('div').children('div').children('.CTWW').text()
        }else if(StudyDes=='MRI'){
            var WC = JSON.parse("[" + $("#frame"+name.toString()).children('label').children('div').children('div').children('.MRIWC').text() + "]")[z]
            var WW = JSON.parse("[" + $("#frame"+name.toString()).children('label').children('div').children('div').children('.MRIWW').text() + "]")[z]
        }
        
        $("#frame"+name.toString()).children('label').children('div').children('div').children('.WC').text('WC: '+WC)
        $("#frame"+name.toString()).children('label').children('div').children('div').children('.WW').text('WW: '+WW)

        $.ajax({
            type: 'post',
            url: urlname, // this is the mapping between the url and view
            data: {
                'variable': z, // ! here is the magic, your variable gets transmitted to the server
                'CTWC':$("#frame"+name.toString()).children('label').children('div').children('div').children('.CTWC').text(),
                'CTWW':$("#frame"+name.toString()).children('label').children('div').children('div').children('.CTWW').text(),
                'PETWC':$("#frame"+name.toString()).children('label').children('div').children('div').children('.PETWC').text(),
                'PETWW':$("#frame"+name.toString()).children('label').children('div').children('div').children('.PETWW').text(),
                'MRIWC':JSON.parse("[" + $("#frame"+name.toString()).children('label').children('div').children('div').children('.MRIWC').text() + "]")[z],
                'MRIWW':JSON.parse("[" + $("#frame"+name.toString()).children('label').children('div').children('div').children('.MRIWW').text() + "]")[z],
                'plane':$("#frame"+name.toString()).children('label').children('div').children('div').children('.plane').text(),
                'mode':$("#frame"+name.toString()).children('label').children('div').children('div').children('.mode').text(),
                'source':$("[name='group1']:checked").next("label").children('div').children('div').children('.StudyDate').text().toString()+$("[name='group1']:checked").next("label").children('div').children('div').children('.StudyID').text().toString()+$("[name='group1']:checked").next("label").children('div').children('div').children('.SeriesID').text().toString(),
                'target':$("#frame"+name.toString()).children('label').children('div').children('div').children('.StudyDate').text().toString()+$("#frame"+name.toString()).children('label').children('div').children('div').children('.StudyID').text().toString()+$("#frame"+name.toString()).children('label').children('div').children('div').children('.SeriesID').text().toString(),
                'source_variable':$("[name='group1']:checked").next("label").children('div').children('div').children('.z').text(),
                'x': x,
                'y': y,
                'height':$("#frame"+name.toString()).children("label").children('div').children('div').children('img').height(),
                'width':$("#frame"+name.toString()).children("label").children('div').children('div').children('img').width(),
                'ActualCoordinates':ActualCoordinates,
                'drawActualCoordinates':drawActualCoordinates,
                'MRI_CrossLink':$('#MRI_CrossLink').is(':checked'),
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            async:true,
            cache:true,
            success: function(response) {
                $("#frame"+name.toString()).children("label").children('div').children('div').children('img').attr('src',response.dicom_url);
                //$("#frame"+name.toString()).children('label').children('.slider').scrollTop(z*$("#frame"+name.toString()).children('label').children('.slider').height())
            },
        });

    }
    function locationCompute(name,x,y,z){
       
        $.ajax({
            type: 'post',
            url: '{% url "DICOM:convertLocation" %}', // this is the mapping between the url and view
            data: {
                'z': z, // ! here is the magic, your variable gets transmitted to the server
                'plane':$("#frame"+name.toString()).children('label').children('div').children('div').children('.plane').text(),
                'x': x,
                'y': y,
                'imageType':$('#frame'+name.toString()).children('label').children('div').children('div').children('.StudyDes').text(),
                'height':$("#frame"+name.toString()).children("label").children('div').children('div').children('img').height(),
                'width':$("#frame"+name.toString()).children("label").children('div').children('div').children('img').width(),
                'PETWC':$("#frame"+name.toString()).children('label').children('div').children('div').children('.PETWC').text(),
                'WindowNo':$("#frame"+name.toString()).children('label').children('div').children('div').children('.series').text(),
                'source':$("[name='group1']:checked").next("label").children('div').children('div').children('.StudyDate').text().toString()+$("[name='group1']:checked").next("label").children('div').children('div').children('.StudyID').text().toString()+$("[name='group1']:checked").next("label").children('div').children('div').children('.SeriesID').text().toString(),
                'target':$("#frame"+name.toString()).children('label').children('div').children('div').children('.StudyDate').text().toString()+$("#frame"+name.toString()).children('label').children('div').children('div').children('.StudyID').text().toString()+$("#frame"+name.toString()).children('label').children('div').children('div').children('.SeriesID').text().toString(),
                'source_variable':$("[name='group1']:checked").next("label").children('div').children('div').children('.z').text(),
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success: function(response) {
                x=response.x
                y=response.y
                z=response.z
                
                $("#frame"+name.toString()).children('label').children('div').children('div').children('.x').text(response.x)
                $("#frame"+name.toString()).children('label').children('div').children('div').children('.y').text(response.y)
                $("#frame"+name.toString()).children('label').children('div').children('div').children('.z').text(response.z)

                DrawWithMouse(x,y,z,name)
                
            }
        });
    }
    function checkPlaneXYZ(frame,x,y,z){
         if(frame=='Axial'){
            frame1_x=x
            frame1_y=y
            frame1_z=z
        }else if(frame=='Coronal'){
            frame1_x=x
            frame1_y=z
            frame1_z=y
        }else if(frame=='Sagittal'){
            frame1_x=y
            frame1_y=z
            frame1_z=x
        }
        return {'x':frame1_x,'y':frame1_y,'z':frame1_z}
    }
    function draw(){
        $("[name='location']:checked").next('label').css('background-color','#e78632')
        
        var indices=$("[name='location']").not(':checked')

        for(var i =0;i<indices.length;i++){

            if (indices.eq(i).next('label').children('.indices').text()==0) {
                indices.eq(i).next('label').css('background-color', '#BBBBBB')
            }else if(indices.eq(i).next('label').children('.indices').text()==1) {
                indices.eq(i).next('label').css('background-color','#A8D8B9')
            }else if(indices.eq(i).next('label').children('.indices').text()==2){
                indices.eq(i).next('label').css('background-color','#81C7D4')
            }else if(indices.eq(i).next('label').children('.indices').text()==3){
                indices.eq(i).next('label').css('background-color','#808F7C')
            }
        }

        ActualCoordinates=true
        strAry=($("[name='location']:checked").next('label').children('.info').text())
        a=strAry.split(',')
        x=a[0]
        y=a[1]
        z=a[2].split('--')[0]

        var SD=$("[name='location']:checked").next('label').children('.LocalSeriesID').text()
        var Date=$("[name='location']:checked").next('label').children('.LocalStudyDate').text()
        var StudyID=$("[name='location']:checked").next('label').children('.LocalStudyID').text()
        var Con=[]
        for(var i =0;i<4;i++) {
            Con.push($('.StudyDate').eq(i).text()+$('.StudyID').eq(i).text()+$('.SeriesID').eq(i).text())
        }

        for(var i =0;i<4;i++) {
            if(Con[i]==Date+StudyID+SD){
                var ind=i+1
               
                frame=$("#frame"+ind).children('label').children('div').children('#dicom'+ind).children('.plane').text()
                frameXYZ=checkPlaneXYZ(frame,x,y,z)
                //ajax_connect_view(ind)
                //$('#frame'+ind).children('label').children('.slider').scrollTop(b)
                ajax(ind,frameXYZ['x'],frameXYZ['y'],frameXYZ['z'],true,true)

                $("#frame"+ind).children('label').children('.slider').scrollTop(frameXYZ['z']*$("#frame"+ind).children('label').children('.slider').height())
                $('#frame'+ind).children('label').children('div').children('div').children('.x').text(x)
                $('#frame'+ind).children('label').children('div').children('div').children('.y').text(y)
                $('#frame'+ind).children('label').children('div').children('div').children('.z').text(z)
                let height=$('#frame'+ind).children('label').children('.slider').height();
                let num = Math.ceil($('#frame'+ind).children('label').children('.slider').children().height()/height)
                
                $('#frame'+ind).children('label').children('div').children('div').children('.variable').text(parseInt(frameXYZ['z'])+1+'/'+num)
            }
        }
    }

    function DrawWithMouse(x,y,z,name){
        ActualCoordinates=true

        scrolling=false
        let imageType = $('#frame'+name).children('label').children('div').children('div').children('.StudyDes').text()
        var Con=[]
        if (imageType != 'MRI'){
            for(var i =0;i<4;i++) {
                Con.push($('.StudyDes').eq(i).text()+'_'+$('.StudyID').eq(i).text()+'_'+$('.StudyDate').eq(i).text()+'_'+$('.SeriesID').eq(i).text())
            }
        }else{
            for(var i =0;i<4;i++) {
                Con.push($('.StudyDes').eq(i).text()+'_'+$('.StudyID').eq(i).text()+'_'+$('.StudyDate').eq(i).text()+'_'+$('.SeriesID').eq(i).text()[1])
            }
        }


        for(var i =0;i<4;i++) {
            if(Con[i]==Con[name-1]){
                var ind=i+1

                frame=$("#frame"+ind).children('label').children('div').children('#dicom'+ind).children('.plane').text()

                let height=Math.floor($('#frame'+ind).children('label').children('.slider').height());
                let num = Math.floor($('#frame'+ind).children('label').children('.slider').children().height()/height)
                let imageType = $('#frame'+ind).children('label').children('div').children('div').children('.StudyDes').text()

                if (imageType == 'MRI'){
                   // alert($("#frame"+ind).children('label').children('div').children('div').children('.StudyDate').text().toString()+$("#frame"+name.toString()).children('label').children('div').children('div').children('.StudyID').text().toString()+$("#frame"+name.toString()).children('label').children('div').children('div').children('.SeriesID').text().toString())
                    $.ajax({
                        type: 'post',
                        url: '{% url "DICOM:convert_MRI_coordinate" %}', // this is the mapping between the url and view
                        data: {
                            'ind':ind,
                            'source':$("[name='group1']:checked").next("label").children('div').children('div').children('.StudyDate').text().toString()+$("[name='group1']:checked").next("label").children('div').children('div').children('.StudyID').text().toString()+$("[name='group1']:checked").next("label").children('div').children('div').children('.SeriesID').text().toString(),
                            'target':$("#frame"+ind).children('label').children('div').children('div').children('.StudyDate').text().toString()+$("#frame"+ind).children('label').children('div').children('div').children('.StudyID').text().toString()+$("#frame"+ind).children('label').children('div').children('div').children('.SeriesID').text().toString(),
                            'source_variable':$("[name='group1']:checked").next("label").children('div').children('div').children('.z').text(),
                            'x': x,
                            'y': y,
                            'z': z,
                            'csrfmiddlewaretoken': window.CSRF_TOKEN
                        },
                        success: function (response) {
                            $("#frame"+response.ind).children('label').children('div').children('#dicom'+response.ind).children('.x').text(response.x)
                            $("#frame"+response.ind).children('label').children('div').children('#dicom'+response.ind).children('.y').text(response.y)
                            $("#frame"+response.ind).children('label').children('div').children('#dicom'+response.ind).children('.z').text(response.z)
                            $("#frame"+response.ind).children('label').children('.slider').scrollTop(response.z*$("#frame"+response.ind).children('label').children('.slider').height())
                            $('#frame'+response.ind).children('label').children('div').children('div').children('.variable').text(response.z+1+'/'+num)
                            ajax(response.ind,response.x,response.y,response.z,true,true)
                        }
                    });
                }else{
                    frameXYZ=checkPlaneXYZ(frame,x,y,z)
                    ajax(ind,frameXYZ['x'],frameXYZ['y'],frameXYZ['z'],true,true)
                    $("#frame"+ind).children('label').children('div').children('#dicom'+ind).children('.x').text(x)
                    $("#frame"+ind).children('label').children('div').children('#dicom'+ind).children('.y').text(y)
                    $("#frame"+ind).children('label').children('div').children('#dicom'+ind).children('.z').text(z)
                    $("#frame"+ind).children('label').children('.slider').scrollTop(frameXYZ['z']*$("#frame"+ind).children('label').children('.slider').height())
                    $('#frame'+ind).children('label').children('div').children('div').children('.variable').text(parseInt(frameXYZ['z'])+1+'/'+num)
                }
            }
        }

    }
    function showReport(){
        if($("[name='Report']:checked").length>4){
            $('#'+event.target.id).prop('checked',false)
        }
        $("[name='Report']:checked").parents('td').css('background-color','#e78632')
        $("[name='Report']:not(':checked')").parents('td').css('background-color','#eeefef')
        for (var i = 0; i < $("[name='Report']:checked").length; i++) {
            var text =$("[name='Report']:checked").eq(i).prev('label').children('.examDate').text()+'\n'+'\n'
            text=text+$("[name='Report']:checked").eq(i).prev('label').children('.examReport').text()
            $('#T'+(i+1)).text(text)
        }

        if($("[name='Report']:checked").length==1){
            $('#T1').css('width','100%')
            $('#T1').css('height','100%')
            $('#T2').css('display','none')
            $('#T3').css('display','none')
            $('#T4').css('display','none')
        }
        if($("[name='Report']:checked").length==2){

            $('#T1').css('width','100%')
            $('#T1').css('height','50%')
            $('#T2').css('width','100%')
            $('#T2').css('height','50%')
            $('#T2').css('display','inline')
            $('#T3').css('display','none')
            $('#T4').css('display','none')
        }
        if($("[name='Report']:checked").length==3){

            $('#T1').css('width','100%')
            $('#T1').css('height','33%')
            $('#T2').css('width','100%')
            $('#T2').css('height','33%')
            $('#T2').css('display','inline')
            $('#T3').css('width','100%')
            $('#T3').css('height','34%')
            $('#T3').css('display','inline')
            $('#T4').css('display','none')
        }
        if($("[name='Report']:checked").length==4){

            $('#T1').css('width','100%')
            $('#T1').css('height','25%')
            $('#T2').css('width','100%')
            $('#T2').css('height','25%')
            $('#T2').css('display','inline')
            $('#T3').css('width','100%')
            $('#T3').css('height','25%')
            $('#T3').css('display','inline')
            $('#T4').css('width','100%')
            $('#T4').css('height','25%')
            $('#T4').css('display','inline')
        }
    }
    function localmaxclick(name){
        var lx=$(event.target).next('label').children('.Localmax_x').text()
        var ly=$(event.target).next('label').children('.Localmax_y').text()
        var lz=$(event.target).next('label').children('.Localmax_z').text()
        var lsuv=$(event.target).next('label').children('.Localmax_SUV').text()
        var Con=[]
        for(var i =0;i<4;i++) {
            Con.push($('.StudyID').eq(i).text()+$('.StudyDate').eq(i).text()+$('.SeriesID').eq(i).text())
        }
        for(var i =0;i<4;i++) {
            if(Con[i]==Con[name-1]){
                var ind=i+1
                $('#frame'+ind).children('label').children('div').children('div').children('.x').text(lx)
                $('#frame'+ind).children('label').children('div').children('div').children('.y').text(ly)
                $('#frame'+ind).children('label').children('div').children('div').children('.z').text(lz)
                $('#frame'+ind).children('label').children('div').children('div').children('.SUV').val(lsuv)
            }
        }


        DrawWithMouse(lx,ly,lz,name)
    }
    function window_load(){
        var ExecDate = $(event.target).parents('.col').parents('.row').prevAll('.row2').children('.ImageExecDate').html()
        StudyDes = $(event.target).parents('.col').parents('.row').prevAll('.row2').children('.ImageStudyDes').html().replaceAll(' ','')
        var StudyID = $(event.target).parents('.col').parents('.row').prevAll('.row2').children('.ImageStudyID').html()
        var SeriesID = $(event.target).parents('.col').parents('.row').prevAll('.row2').children('.ImageSeriesID').html()
        var SeriesDes = $(event.target).parents('.col').parents('.row').prevAll('.row2').children('.ImageSeriesDes').html()
        var PID = $('#PIDText').text()
        var WindowNo = $(event.target).attr('name')

        var STD = $('#frame'+WindowNo).children('label').children('.main').children('div').children('.StudyDate').text()
        var STID = $('#frame'+WindowNo).children('label').children('.main').children('div').children('.StudyID').text()
        
        if((STID+STD)!=(StudyID+ExecDate)){
            $.ajax({
                type: 'post',
                url: '{% url "DICOM:window_load" %}', // this is the mapping between the url and view
                data:{
                    'WindowNo':WindowNo,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN
                },
            })
        }
        $('#frame'+WindowNo).children('label').children('.main').children('div').children('.img').css('width','100%')
        $('#frame'+WindowNo).children('label').children('.main').children('div').children('.img').css('height','100%')
        $('#frame'+WindowNo).children('label').children('.main').children('div').children('.StudyDate').text(ExecDate)
        $('#frame'+WindowNo).children('label').children('.main').children('div').children('.StudyID').text(StudyID)
        $('#frame'+WindowNo).children('label').children('.main').children('div').children('.SeriesID').text(SeriesID)
        $('#frame'+WindowNo).children('label').children('.main').children('div').children('.SeriesDes').text(SeriesDes)
        $('#frame'+WindowNo).children('label').children('.main').children('div').children('.StudyDes').text(StudyDes)
        
        $('#frame'+WindowNo).children('label').children('.slider').css('display','none');
        $('#frame'+WindowNo).children('label').children('.main').children('.loader').css('display','inline')
        $('#frame'+WindowNo).children("label").children('div').children('div').children('img').css('display','none')
        $('.loader').css('top',$("#frame1").height()/2)
        

        var str=$('.StudyID').eq(0).text()+'_'+$('.SeriesID').eq(0).text()
        for(var i =1;i<$('.SeriesID').length;i++){
            str+=','+$('.StudyID').eq(i).text()+'_'+$('.SeriesID').eq(i).text()
        }
        var Study_Date=$('.StudyDate').eq(0).text()
        for(var i =1;i<$('.StudyDate').length;i++){
            Study_Date+=','+$('.StudyDate').eq(i).text()
        }
        if(StudyDes=='PET'){
            loadDICOMurlname="{% url 'DICOM:load_DICOM' %}"
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.StudyDes').text('PET')
            $("#frame"+WindowNo).children('label').children('div').children('div').children('.mode').text('Fusion')
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.LocalMax').text(true)
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.LocalMax_disable').text(false)
        }else if(StudyDes=='RTPLAN'){
            loadDICOMurlname="{% url 'DICOM:load_RT_DICOM' %}"
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.StudyDes').text('RTPLAN')
            $("#frame"+WindowNo).children('label').children('div').children('div').children('.mode').text('CT')
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.LocalMax').text(false)
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.LocalMax_disable').text(true)
        }else if(StudyDes=='CT'){
            loadDICOMurlname="{% url 'DICOM:load_CT_DICOM' %}"
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.StudyDes').text('CT')
            $("#frame"+WindowNo).children('label').children('div').children('div').children('.mode').text('CT')
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.LocalMax').text(false)
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.LocalMax_disable').text(true)
        }else if(StudyDes=='MRI'){
            loadDICOMurlname="{% url 'DICOM:load_MRI_DICOM' %}"
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.StudyDes').text('MRI')
            $("#frame"+WindowNo).children('label').children('div').children('div').children('.mode').text('CT')
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.LocalMax').text(false)
            $('#frame'+WindowNo).children('label').children('div').children('div').children('.LocalMax_disable').text(true)
        }
        $.ajax({
            type: 'post',
            url: loadDICOMurlname, // this is the mapping between the url and view
            data:{
                'StudyDes':StudyDes,
                'WindowNo':WindowNo,
                'root':root,
                'PID':PID,
                'MedExecTime':ExecDate,
                'StudyIDText':StudyID,
                'SeriesIDText':SeriesID,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success:function (response) {
                $('#RT_Contour').empty()
                if(StudyDes=='RTPLAN'){
                    $.ajax({
                        type: 'post',
                        url: '{% url "DICOM:ROIname" %}', // this is the mapping between the url and view
                        data: {
                            'WindowNo': WindowNo, // ! here is the magic, your variable gets transmitted to the server
                            'csrfmiddlewaretoken': window.CSRF_TOKEN
                        },
                        success: function(response) {
                            $('#RT_Contour').empty()
                            for(var i =0;i<response.ROIname.length;i++) {
                                
                                $('#RT_Contour').append('' +
                                    '<div class="form-check form-switch">' +
                                        '<input class="form-check-input" onchange="drawContour()" type="checkbox" name="RT" id="'+response.ROIname[i]+'">' +
                                        '<label class="form-check-label" for="'+response.ROIname[i]+'">' + response.ROIname[i] + '</label>' +
                                        '<div style="display:inline-block;position:absolute;right: 0px ;width:20px;height: 20px;background-color: rgb('+response.color[i]+')"></div>' +
                                    '</div>' +
                                '')
                            }
                        },
                    });
                }else if(StudyDes=='MRI'){
                    $('#MRIWC').val(response.MRIWC[0])
                    $('#MRIWW').val(response.MRIWW[0])
                    $("#frame"+WindowNo.toString()).children('label').children('div').children('div').children('.MRIWC').text(response.MRIWC.toString())
                    $("#frame"+WindowNo.toString()).children('label').children('div').children('div').children('.MRIWW').text(response.MRIWW.toString())
                    $("#frame"+WindowNo.toString()).children('label').children('div').children('div').children('.WC').text('WC: '+response.MRIWC[0])
                    $("#frame"+WindowNo.toString()).children('label').children('div').children('div').children('.WW').text('WW: '+response.MRIWW[0])
                }
                $('.loader').css('display','none')
                if(WindowNo==1){
                    urlname="{% url 'DICOM:DICOM_show1' %}"
                }else if(WindowNo==2){
                    urlname="{% url 'DICOM:DICOM_show2' %}"
                }else if(WindowNo==3) {
                    urlname="{% url 'DICOM:DICOM_show3' %}"
                }else if(WindowNo==4){
                    urlname="{% url 'DICOM:DICOM_show4' %}"
                }
                name=WindowNo
                $("#frame"+name.toString()).children("label").children('div').children('div').children('img').css('display','inline-block');
                $("#frame"+name.toString()).children("label").children('.slider').css('display','inline-block');
                $('#frame'+WindowNo).children('input').prop('checked',true)
                //$('#viewPlane').val('Axial').prop('selected',true);
                //alert($("[name='group1']:checked").next("label").children('div').children('div').children('.series').text())
                $.ajax({
                    type: 'post',
                    url: urlname, // this is the mapping between the url and view
                    data: {
                        'variable': 0, // ! here is the magic, your variable gets transmitted to the server
                        'CTWC':$("#frame"+name.toString()).children('label').children('div').children('div').children('.CTWC').text(),
                        'CTWW':$("#frame"+name.toString()).children('label').children('div').children('div').children('.CTWW').text(),
                        'PETWC':$("#frame"+name.toString()).children('label').children('div').children('div').children('.PETWC').text(),
                        'PETWW':$("#frame"+name.toString()).children('label').children('div').children('div').children('.PETWW').text(),
                        'MRIWC':JSON.parse("[" + $("#frame"+name.toString()).children('label').children('div').children('div').children('.MRIWC').text() + "]")[0],
                        'MRIWW':JSON.parse("[" + $("#frame"+name.toString()).children('label').children('div').children('div').children('.MRIWW').text() + "]")[0],
                        'plane':$("#frame"+name.toString()).children('label').children('div').children('div').children('.plane').text(),
                        'mode':$("#frame"+name.toString()).children('label').children('div').children('div').children('.mode').text(),
                        'source':$("[name='group1']:checked").next("label").children('div').children('div').children('.StudyDate').text()+$("[name='group1']:checked").next("label").children('div').children('div').children('.StudyID').text()+$("[name='group1']:checked").next("label").children('div').children('div').children('.SeriesID').text(),
                        'target':$("#frame"+name.toString()).children('label').children('div').children('div').children('.StudyDate').text()+$("#frame"+name.toString()).children('label').children('div').children('div').children('.StudyID').text()+$("#frame"+name.toString()).children('label').children('div').children('div').children('.SeriesID').text(),
                        'source_variable':$("[name='group1']:checked").next("label").children('div').children('div').children('.z').text(),
                        'x': 0,
                        'y': 0,
                        'height':$("#frame"+name.toString()).children("label").children('div').children('div').children('img').height(),
                        'width':$("#frame"+name.toString()).children("label").children('div').children('div').children('img').width(),
                        'ActualCoordinates':true,
                        'drawActualCoordinates':true,
                        'csrfmiddlewaretoken': window.CSRF_TOKEN
                    },
                    success: function(response) {
                        $('#frame'+name.toString()).children('label').children('.main').children('div').children('.thickness').text(response.thickness+'mm')
                        $("#frame"+name.toString()).children("label").children('div').children('div').children('img').attr('src',response.dicom_url);
                        z=response.z
                        $("#frame"+name.toString()).children('label').children('.slider').children('div').css('height',z*100+'%')
                        $('#frame'+name.toString()).children('label').children('.slider').scrollTop(0)
                        $('#frame'+name.toString()).children('label').children('div').children('div').children('.variable').text(1+'/'+z)
                        mouseover()
                        
                    },
                    complete:function(){
                        selection()
                        let window_sno = $("[name='group1']:checked").next("label").children('div').children('div').children('.series').text()
                        functionAjax=[ajax1(),ajax2(),ajax3(),ajax4()]
                        functionAjax[window_sno]
                    }
                });
                selectLocation()
            }
        });
    }

    //畫RT影像
    function drawContour(){
        var ROIname=[]
        var Color=[]
        for(var i=0;i<$('input[name="RT"]:checked').length;i++){
            ROIname.push($('input[name="RT"]:checked').eq(i).next('label').html())
            Color.push($('input[name="RT"]:checked').eq(i).nextAll('div').css('background-color'))
        }

        $.ajax({
            type: 'post',
            url: '{% url "DICOM:DrawContour" %}', // this is the mapping between the url and view
            data:{
                'WindowNo':$("[name='group1']:checked").next("label").children('div').children('div').children('.series').text(),
                'ROIname':ROIname,
                'Color':Color,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            }
        })
    }
    function CTWindow_menu(){
        var CT_window = $('#CTWindow_menu option:selected').val()
        $('#CTWindow').val(CT_window).prop('selected',true);
        dicomwindow()
    }
    function Mode_menu(){
        var Mode = $('#Mode_menu option:selected').val()
        $('#Mode').val(Mode).prop('selected',true);
        dicomwindow()
    }
    function Plane_menu(){
        var viewPlane = $('#Plane_menu option:selected').val()
        $('#viewPlane').val(viewPlane).prop('selected',true);
        dicomwindow()
    }


    function right_function(e){
        var x = e.originalEvent.x || e.originalEvent.layerX || 0;
        var y = e.originalEvent.y || e.originalEvent.layerY || 0;
        $("#image_menu").css('display', 'inline');
        $("#image_menu").css('left', x);
        $("#image_menu").css('top', y);
    }
    const handleWheel = function(e) {
        if(e.ctrlKey || e.metaKey)
            e.preventDefault();
    };
    window.addEventListener("wheel", handleWheel, {passive: false});

    

    function UNet(){
        let id = $('input[name="location"]:checked').next('label').children('.deleteInfo').text();
        let position = $('input[name="location"]:checked').next('label').children('.info').text();
        let plane = $("[name='group1']:checked").next("label").children('div').children('div').children('.plane').text();
        let WindowNo = $("[name='group1']:checked").next("label").children('div').children('div').children('.series').text()
        let x = position.split(',')[0];
        let y = position.split(',')[1];
        let z = position.split(',')[2];
        $.ajax({
            type: 'post',
            url: '{% url "DICOM:UNet" %}', // this is the mapping between the url and view
            data:{
                'id':id,
                'WindowNo':WindowNo,
                'plane':plane,
                'x':x,
                'y':y,
                'z':z,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },success:function(){
                $("#location_menu").css('display', 'none')
                let SD=$("[name='location']:checked").next('label').children('.LocalSeriesID').text()
                let Date=$("[name='location']:checked").next('label').children('.LocalStudyDate').text()
                let StudyID=$("[name='location']:checked").next('label').children('.LocalStudyID').text()
                let ActualCoordinates=true
                let Con=[]
                for(var i =0;i<4;i++) {
                    Con.push($('.StudyDate').eq(i).text()+$('.SeriesID').eq(i).text())
                }
                for(var i =0;i<4;i++) {
                    if(Con[i]==Date+SD){
                        var ind=i+1
                        
                        frame=$("#frame"+ind).children('label').children('div').children('#dicom'+ind).children('.plane').text()
                        frameXYZ=checkPlaneXYZ(frame,x,y,z)
                        ajax(ind,frameXYZ['x'],frameXYZ['y'],frameXYZ['z'],true,true)
                        $("#frame"+ind).children('label').children('.slider').scrollTop(frameXYZ['z']*$("#frame"+ind).children('label').children('.slider').height())
                        $('#frame'+ind).children('label').children('div').children('div').children('.x').text(x)
                        $('#frame'+ind).children('label').children('div').children('div').children('.y').text(y)
                        $('#frame'+ind).children('label').children('div').children('div').children('.z').text(z)
                        let height=$('#frame'+ind).children('label').children('.slider').height();
                        let num = Math.ceil($('#frame'+ind).children('label').children('.slider').children().height()/height)
                        $('#frame'+ind).children('label').children('div').children('div').children('.variable').text(parseInt(frameXYZ['z'])+1+'/'+num)
                    }
                }
            }
        })
    }

    function selectLocation(){
        PID = $('#PIDText').text()

        var str=$('.StudyID').eq(0).text()+'_'+$('.SeriesID').eq(0).text()
        for(var i =1;i<$('.SeriesID').length;i++){
            str+=','+$('.StudyID').eq(i).text()+'_'+$('.SeriesID').eq(i).text()
        }
        var Study_Date=$('.StudyDate').eq(0).text()
        for(var i =1;i<$('.StudyDate').length;i++){
            Study_Date+=','+$('.StudyDate').eq(i).text()
        }
        $.ajax({
            type: 'post',
            url: '{% url "DICOM:selectLocation" %}', // this is the mapping between the url and view
            data: {
                'PID': PID,
                'Disease':$('#Disease').val(),
                'username':$('#users option:selected').text(),
                'date':Study_Date,
                'str':str,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success: function (response) {

                $('#textarea').children('tr').remove();
                
                for (var i = 0; i < response.PID.length; i++) {
                    $('#textarea').append('<tr><td><input onclick="draw()" type="radio" name="location" id=' + i + '>' +
                        '<label for=' + i + '>' +
                        '<p class="deleteInfo">' + response.id[i] + '</p>' +
                        '<p class="info">' + response.x[i] + ',' + response.y[i] + ',' + response.z[i]+'</p><p class="data">'+response.SUV[i] + '</p>' +
                        '<p class="data1">StudyID:' + response.StudyID[i] +'</p>'+
                        '<p class="data1">SeriesID:' + response.SeriesID[i] +'</p>'+
                        '<p class="data1">' + response.LabelGroup[i] +'</p>'+
                        '<p class="data1">' + response.LabelName[i] +'</p>'+
                        '<p class="data1">' + response.LabelRecord[i] +'</p>'+
                        '<p class="LocalStudyID">' + response.StudyID[i] +'</p>'+
                        '<p class="LocalSeriesID">' + response.SeriesID[i] +'</p>'+
                        '<p class="LocalStudyDate">' + response.SD[i] +'</p>'+
                        '<p class="indices">' + response.indices[i] +'</p>'+
                        '</label></td></tr>')
                    
                    if (response.indices[i]==0) {
                        $('#' + i).next('label').css('background-color', '#BBBBBB')
                    }else if(response.indices[i]==1) {
                        $('#'+i).next('label').css('background-color','#A8D8B9')
                    }else if(response.indices[i]==2){
                        $('#'+i).next('label').css('background-color','#81C7D4')
                    }else if(response.indices[i]==3){
                        $('#'+i).next('label').css('background-color','#808F7C')
                    }
                }
                $('.localizationform').scrollTop($('#textarea').height())
            },
        });
    }

    function SaveCoordinate(){
        let PID = $("[name='group1']:checked").next("label").children('div').children('div').children('.PID').text()
        let StudyID = $("[name='group1']:checked").next("label").children('div').children('div').children('.StudyID').text()
        let SeriesID = $("[name='group1']:checked").next("label").children('div').children('div').children('.SeriesID').text()
        let variable = Math.floor($("[name='group1']:checked").next("label").children('.slider').scrollTop()/Math.floor($("[name='group1']:checked").next("label").children('.slider').height()))
        let username = JSON.parse(document.getElementById('user_username').textContent)
        let Disease = $('#Disease').val()
        let date = $("[name='group1']:checked").next("label").children('div').children('div').children('.StudyDate').text()
        let LabelRecord = $('#MRI_LabelRecord').val()
        $.ajax({
            type: 'post',
            url: '{% url "DICOM:SaveCoordinate" %}', // this is the mapping between the url and view
            data: {
                'PID':PID,
                'StudyID':StudyID,
                'SeriesID':SeriesID,
                'variable':variable,
                'username':username,
                'Disease':Disease,
                'date':date,
                'LabelRecord':LabelRecord,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success: function(response) {

                selectLocation()
            },
        });
    }

    function getuser(){
        let username = JSON.parse(document.getElementById('user_username').textContent)
        $.ajax({
            type: 'post',
            url: '{% url "DICOM:getusers" %}', // this is the mapping between the url and view
            data: {
                'username':username,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success: function(response) {
                
                for(var i=0;i<response.users.length;i++){
                    $('#users').append('<option >'+response.users[i]+'</option>')
                    if(response.users[i]==username){
                        $('#users').children('option').eq(i).prop('selected',true)
                    }
                }
                if(response.is_superuser){
                    $('#users').css({
                        'z-index': '2',
                        'position': 'fixed',
                        'height': '40px',
                        'top': '95px',
                        'width': '9.9%',
                        'margin': '0px',
                        'right': '20%',
                        'border-radius': '0px 0px 5px 5px'
                    })
                    $('.localizationform').css({
                        'position': 'fixed',
                        'height': 'calc(100% - 130px)', 
                        'top': '130px',  
                        'right': '20%'
                    })
                }
            }
        });
    }

    