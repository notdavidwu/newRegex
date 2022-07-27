function setdisplay(i){
        
    //if($('#timePID'+i).next('label').height()> $('#timePID'+i).next('label').children('.note').height()&& $('#timePID'+i).next('label').height()>$('#timePID'+i).next('label').children('.type2').height()){
    //    $('#timePID'+i).next('label').prev().parents('td').css('height',$('#timePID'+i).next('label').height()+22)
    //    $('#timePID'+i).next('label').css('height',$('#timePID'+i).next('label').height()+22)
    //    $('#timePID'+i).next('label').children('.note').css('margin-top',($('#timePID'+i).parents().height()-$('#timePID'+i).next('label').children('.note').height())/2)
    //    $('#timePID'+i).next('label').children('.Ignore').css('height',$('#timePID'+i).next('label').children('.type2').height()+5)
    //    console.log(1)
    //}else if($('#timePID'+i).next('label').children('.note').height()>$('#timePID'+i).next('label').children('.type2').height()){
    //    $('#timePID'+i).next('label').prev().parents('td').css('height',$('#timePID'+i).next('label').children('.note').height()+22)
    //    $('#timePID'+i).next('label').css('height',$('#timePID'+i).next('label').children('.note').height()+22)
    //    $('#timePID'+i).next('label').children('.Ignore').css('height',$('#timePID'+i).next('label').children('.note').height()+5)
    //    $('#timePID'+i).next('label').children('.note').css('margin-top',($('#timePID'+i).parents().height()-$('#timePID'+i).next('label').children('.note').height())/2)
    //    console.log(2)
    //}else if($('#timePID'+i).next('label').children('.note').height()<$('#timePID'+i).next('label').children('.menu').height()){
    //    $('#timePID'+i).next('label').prev().parents('td').css('height',$('#timePID'+i).next('label').children('.menu').height()+22)
    //    $('#timePID'+i).next('label').css('height',$('#timePID'+i).next('label').children('.menu').height())
    //    $('#timePID'+i).next('label').children('.note').css('margin-top',($('#timePID'+i).parents().height()-$('#timePID'+i).next('label').children('.note').height())/2)
    //    console.log(3)
    //}
    $('#timePID'+i).next('label').css('height',$('#timePID'+i).next('label').children('.menu').height()+10)
    $('#timePID'+i).next('label').css('height',$('#timePID'+i).next('label').children('.menu').height()+10)
    $('#timePID'+i).next('label').children('.accordion').css('height',$('#timePID'+i).next('label').height())    

}
function addPhaseAndSeq(pannel,medType,seqNoOption,appendOrPrepend){
    let selection = getClinicalProcedures(medType)
    let addObject = '<div class=menublock id="sno_-1_0_-1_0">'+
        '<select onchange="UpdateInterval()" class="IntervalNo  form-select form-select-sm" aria-label=".form-select-sm example">'+seqNoOption+'</select>'+
        '<select onchange="UpdatePhase()" class="phase form-select form-select-sm" aria-label=".form-select-sm example">'+selection+'</select>'+
        '</div>'
    if(appendOrPrepend=='append'){
        $('#'+pannel).next('label').children('.menu').append(addObject)
    }else{
        $('#'+pannel).next('label').children('.menu').children('.addButton').before(addObject)
    }           
}

function getClinicalProcedures(medType){
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getClinicalProcedures" %}', // this is the mapping between the url and view
        data:{
            'medType':medType,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        async:false,
        success:function (response){
            selection = response.selection
        }
    })
    return selection
}

function addMenu(){
    let id = $(event.target).parents('label').prevAll('input').attr('id')
    let medType = $(event.target).parents('.menu').prevAll('.medType').html()
    let IND = id.split('timePID')[1]
    addPhaseAndSeq(id,medType,seqNoOption,'prepend')
    let target = $(`#${id}`).next('label').children('.menu').children('div')

    if("{{eventDefinition_edit}}"=='False' ){
        target.eq(target.length-2).children('.phase').prop('disabled',true)
        target.eq(target.length-2).children('.IntervalNo').prop('disabled',true)
    }else{
        target.eq(target.length-2).children('.phase').prop('disabled',false)
        target.eq(target.length-2).children('.IntervalNo').prop('disabled',false)
    }

    setdisplay(IND)
}

function searchNote(IND,eventID){
    let chartNo= $('input[name="confirmPID"]:checked').next('label').children('.PatientListID').text() 
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:searchNote" %}', // this is the mapping between the url and view
        data:{
            'chartNo':chartNo,
            'IND':IND,
            'eventID':eventID,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            $('#timePID'+response.IND).next('label').children('.note').html(response.object)
        }
    })
    
}
function searchPhaseAndInterval(i,sno){
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:searchPhaseAndInterval" %}', // this is the mapping between the url and view
        data:{
            'sno':sno,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            $('#sno_'+sno).children('.eventGroup').children('option[value='+response.eventNo+']').attr('selected','selected')
            let eventNo = response.eventNo[0]

            if(eventNo!=0){
                $.ajax({
                    type: 'post',
                    url: '{% url "eventDefinition:Phase" %}', // this is the mapping between the url and view
                    data:{
                        'eventNo':eventNo,
                        'csrfmiddlewaretoken': window.CSRF_TOKEN
                    },
                    success:function (response){

                        $('#sno_'+sno).children('.phase').empty()
                        $('#sno_'+sno).children('.phase').append(response.phase)
                    }
                })
            }
            if(i==total_num-1){
                $('#timetable').css('visibility','visible')
                $('.loader2').css('display','none')
            }
            
        },
        complete:function(response){
            $('#sno_'+sno).children('.phase').children('option[value='+response.eventTag+']').attr('selected','selected')
            $('#sno_'+sno).children('.IntervalNo').children('option[value='+response.seqNo+']').attr('selected','selected')
            
        }
    })

}
function searchRecord(IND,eventID,medType,seqNoOption,total){
    let chartNo=$('input[name=confirmPID]:checked').next('label').children('.PatientListID').text()
    let username = '{{user.username}}'
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:searchRecord" %}', // this is the mapping between the url and view
        data:{
            'IND':IND,
            'chartNo':chartNo,
            'eventID':eventID,
            'username':username,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){

            for(var i =0 ;i<response.Record;i++){
                let id = 'timePID'+IND.toString()
                addPhaseAndSeq(id,medType,seqNoOption,'append')
                let RecordedID=`sno_${response.EDID[i]}_${response.eventID_F[i]}_${response.PDID[i]}_${response.caSeqNo[i]}`
                
                $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).attr('id',RecordedID)
                $(`#${RecordedID}`).children('.phase').children('option[value='+response.procedureID[i]+']').attr('selected','selected')
                $(`#${RecordedID}`).children('.IntervalNo').children('option[value='+response.caSeqNo[i]+']').attr('selected','selected') 
                //console.log(response.editor[i],'{{user.username}}')

                //檢查是不是癌登尚未確認的資料
                if(response.eventID[i]==null){
                    $(`#timePID${IND}`).attr('class','sno_'+response.EDID[i])
                    $(`#timePID${IND}`).parent().css('background-color','#4D5139')
                    $(`#timePID${IND}`).parent().css('color','#FFFFFF')
                }
                
                if("{{eventDefinition_edit}}"=='False'){
                    $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).children('.phase').prop('disabled',true)
                    $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).children('.IntervalNo').prop('disabled',true)
                }else if('{{user.is_superuser}}'=='True' ){
                    $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).children('.phase').prop('disabled',false)
                    $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).children('.IntervalNo').prop('disabled',false)
                }else{
                    if(response.editor[i]!=username){
                        $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).children('.phase').prop('disabled',true)
                        $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).children('.IntervalNo').prop('disabled',true)
                    }
                    if(response.editor[i]=='NoRecord'){
                        $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).children('.phase').prop('disabled',false)
                        $(`#timePID${IND}`).next('label').children('.menu').children('div').eq(i).children('.IntervalNo').prop('disabled',false)
                    }
                }
            }
            $('#timePID'+IND.toString()).next('label').children('.menu').append('<div class="addButton"><button type="button" onclick="addMenu()" class="add btn btn-outline-primary">+</button></div>')

            if(IND==(total-1)){
                $('#timetable').css('visibility','visible')
                $('.loader2').css('display','none')
            }
            setdisplay(IND)
        }
    })
    
    
}

function GetTime(){
    
    $('#timetable').css('visibility','hidden')
    $('.loader2').css('display','inline')
    $('.factorGroupArea').empty()
    $('.procedureOfForm').empty()
    $('.formVersion').empty()
    ascriptionClose(detect=true)
    cancerRegistCheckClose()
    patientStatusCheckClose()
    extractedFactorClose()
    text=$('input[name=confirmPID]:checked').next('label').children('.PatientListID').text()
    seqNoOption='<option value=0>?</option>'
    let scrollTop = $('#patient').scrollTop()
    let excludeFilter = $('#excludeFilter').is(':checked')
    
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getSeqNoOption" %}', // this is the mapping between the url and view
        data:{
            'chartNo':text,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            seqNoOption+=response.seqNo
        },
        complete:function(){
            $.ajax({
                type: 'post',
                url: '{% url "eventDefinition:confirmpat2" %}', // this is the mapping between the url and view
                data:{
                    'ID':text,
                    'scrollTop':scrollTop,
                    'excludeFilter':excludeFilter,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN
                },
                success:function (response){
                    $('#time').children('tbody').children('tr').remove()
                    var HeavyDisease=[30001,30002]
                    if(response.objectArray.length!=0){
                        $('#accordionExample').empty()
                        for(var i=0;i<response.objectArray.length;i++){
                            if(response.MedType[i]==30001 || response.MedType[i]==30002){
                                $('#time').append(response.objectArray[i])
                                $('#timePID'+i).parents('td').css('background-color', '#33333a')
                                $('#timePID'+i).next('label').css('color', 'red')
                                setdisplay(i)
                            }else if(response.MedType[i]==1218401){
                                $('#time').append(response.objectArray[i])
                                $('#timePID'+i).parents('td').css('background-color', '#aef2f1')
                            }else{
                                $('#time').append(response.objectArray[i])
                            }
                            
                            searchRecord(i,response.eventID[i],response.MedType[i],seqNoOption,response.objectArray.length)
                        }
                        total_num = response.objectArray.length
                        for(let i=0;i<response.eventID_F.length;i++){
                            let eventIDGroup = $('#timetable .eventID').map(function(){return parseInt($(this).html())}).get()
                            let index = eventIDGroup.indexOf(response.eventID_F[i])
                            let target = $('#timetable .eventID').eq(index)
                            let targetID = $('#timetable .eventID').eq(index).parents('label').prevAll('input').attr('id')
    
                            target.parents('label').append(`<div class="btn btn-primary accordion accordion-toggle" data-bs-toggle="collapse" data-bs-target="#collapse${i}" ></div>`)
                            target.nextAll('.accordion').css('height',target.parents('label').height()+16+'px')
                            addInducedEvent(i,response.eventID_F[i],targetID)
                        }
                    }else{
                        $('#accordionExample').html('<p style="postion:absolute;width:100%;font-size: 40pt;font-weight:700;text-align: center;font-family: font-family: "LiGothic", "FangSong", Arial, serif;">查無資料</p>')
                        $('#timetable').css('visibility','visible')
                        $('.loader2').css('display','none')
                    }
                    $('[data-eventCheck="False"]').parents('td').css('background-color','#D9CD90')
                }
            })
        }
    })
    
    
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getCancerRegistData" %}', // this is the mapping between the url and view
        data:{
            'chartNo':text,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            $('#cancerRegistInfo').children('tbody').empty()
            for(let i=0;i<response.PD.length;i++){
                $('#cancerRegistInfo').children('tbody').append(`<tr><td>${response.PD[i]}</td><td>${response.chartNo[i]}</td><td>${response.disease[i]}</td><td>${response.caSeqNo[i]}</td></tr>`)
            }
        }
    })
    return true
}

function addInducedEvent(i,eventID,index){
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:addInducedEvent" %}', // this is the mapping between the url and view
        data:{
            'ind':i,
            'eventID':eventID,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){

            $(`#${index}`).parents('tr').after(response.objectList)
        }
    })
}
function showReport(){
    $('#text').html($('input[name=timePID]:checked').next('label').children('.report2').text())
}
function GetReport() {
    reporttext=$('input[name=timePID]:checked').next('label').children('.report2').text()
    $('#text').html(reporttext)
    if($('#ascription').css('display')!='none'){
        let pdID = $('input[name="timePID"]:checked').next('label').children('.pdID').html()
        let eventID = $('input[name="timePID"]:checked').next('label').children('.eventID').html()
        let ChartNo = $('input[name="timePID"]:checked').next('label').children('.ChartNo').html()
        let OrderNo = $('input[name="timePID"]:checked').next('label').children('.OrderNo').html()
        let edate = $('input[name="timePID"]:checked').next('label').children('.edate').html()
        let type2 = $('input[name="timePID"]:checked').next('label').children('.type2').html()
        let menublock = $('input[name="timePID"]:checked').next('label').children('.menu').children('.menublock')
        $('#desDate').html(edate)
        $('#desExam').html(type2)
        $('#desPhase').html(menublock.clone(true))
        $('#inductionEventID2').text(eventID)
    }
    
}
function UpdatePhase(){
    target=$(event.target)
    let IND = target.parents('label').prevAll('input').attr('id').split('timePID')[1]
    let EDID = target.parents('.menublock').attr('id').split('_')[1]
    let pdID = target.parents('.menublock').attr('id').split('_')[3]
    let originSeqNo = target.parents('.menublock').attr('id').split('_')[4]
    let eventID = target.parents('.menu').prevAll('.eventID').html()
    let procedureID = target.val()
    let PDIDGroup = $('#accordionExample .menublock').map(function(){return parseInt($(this).attr('id').split('_')[3])}).get()
    let chartNo = target.parents('.menu').prevAll('.ChartNo').html()
    let diseaseId = $('#ChangeDisease').val()
    let username = '{{user.username}}'
    target.css('border','none')
    if(pdID==-1){
        pdID = Math.min(...PDIDGroup.filter(PDID => PDID > 0))
        target.prevAll('.IntervalNo').val(1)
        originSeqNo = 1
    }
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:updatePhase" %}', // this is the mapping between the url and view
        data:{
            'EDID':EDID,
            'PDID':pdID,
            'eventID':eventID,
            'procedureID':procedureID,
            'chartNo':chartNo,
            'diseaseId':diseaseId,
            'originSeqNo':originSeqNo,
            'username':username,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            target.prevAll('.IntervalNo').val(response.originSeqNo)
            target.parents('.menublock').attr('id',`sno_${response.sno}_${eventID}_${response.PDID}_${response.originSeqNo}`)
        }
    })
}


function UpdateInterval(){
    target=$(event.target)
    let IND = target.parents('label').prevAll('input').attr('id').split('timePID')[1]
    let EDID = target.parents('.menublock').attr('id').split('_')[1]
    let pdID = target.parents('.menublock').attr('id').split('_')[3]
    let seqNo = target.val()
    let eventID = target.parents('.menu').prevAll('.eventID').html()
    let procedureID = target.next('.phase').val()
    let PDIDGroup = $('#accordionExample .menublock').map(function(){return parseInt($(this).attr('id').split('_')[3])}).get()
    let chartNo = target.parents('.menu').prevAll('.ChartNo').html()
    let diseaseId = $('#ChangeDisease').val()
    let username = '{{user.username}}'
    target.css('border','none')
    if(pdID==-1){
        target.next('.phase').children('option').eq(1).prop('selected',true)
        procedureID =  target.next('.phase').val()
    }
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:updateInterval" %}', // this is the mapping between the url and view
        data:{
            'EDID':EDID,
            'PDID':pdID,
            'eventID':eventID,
            'procedureID':procedureID,
            'chartNo':chartNo,
            'diseaseId':diseaseId,
            'seqNo':seqNo,
            'username':username,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            target.next('.phase').val(response.procedureID)
            target.parents('.menublock').attr('id',`sno_${response.sno}_${eventID}_${response.PDID}_${response.seqNo}`)
        }
    })
}


function belong(){
    $('#ascription').css('display','inline')
    let inductionID = $('input[name="timePID"]:checked').attr('id')
    let pdID = $('#'+inductionID).next('label').children('.pdID').html()
    let eventID = $('#'+inductionID).next('label').children('.eventID').html()
    let ChartNo = $('#'+inductionID).next('label').children('.ChartNo').html()
    let OrderNo = $('#'+inductionID).next('label').children('.OrderNo').html()
    let edate = $('#'+inductionID).next('label').children('.edate').html()
    let type2 = $('#'+inductionID).next('label').children('.type2').html()
    let menublock = $('#'+inductionID).next('label').children('.menu').children('.menublock')
    $(`label[for=${inductionID}]`).parents('td').css('background-color','#FF0000')

    $('#inductionID').text(inductionID)
    $('#date').html(edate)
    $('#exam').html(type2)
    $('#ascriptionPhase').html(menublock.clone(true))
    $('#inductionEventID1').text(eventID)
    $("#menu").css('display', 'none');
}
function ascriptionClose(detect=false){
    
    if(detect==false){
        let inductionID = $('#inductionID').text()
        $(`label[for=${inductionID}]`).parents('td').css('background-color','transparent') 
    }
    $('#date').empty()
    $('#exam').empty()
    $('#ascriptionPhase').empty()
    $('#inductionEventID1').empty()
    $('#desDate').empty()
    $('#desExam').empty()
    $('#desPhase').empty()
    $('#inductionEventID2').empty()
    $("#ascription").css('display', 'none');
}

function statusOpen(){
    let seq = ''
    for(let i=0;i<=10;i++){seq+=`<option value=${i}>${i}</option>`}
    let chartNo=$('input[name=confirmPID]:checked').next('label').children('.PatientListID').text()
    let diseaseId = $('#ChangeDisease').val()
    $("#patientStatusCheck").css('display', 'inline');
    $("#statusMenu").css('display', 'none');
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getPatientStatus" %}', // this is the mapping between the url and view
        data:{
            'chartNo':chartNo,
            'diseaseId':diseaseId,
        },
        success:function (response){
            $('#statusArea tbody').empty()

            for(let i=0; i<response.PD.length; i++){
                $('#statusArea tbody').append(`
                <tr data-prepareAdd='true' id=${response.PD[i]}>
                    <td><select onchange="updateDiseaseAndSeq()" class="diseaseCheck form-control">${$('#ChangeDisease').html()}</select></td>
                    <td><select onchange="updateDiseaseAndSeq()" class="seqCheck form-control">${seq}</select></td>
                    <td><input type="checkbox" onclick="excludeCheck('statusArea')" class="diagChecked" name=${response.PD[i]}></td>
                    <td><input type="checkbox" onclick="excludeCheck('statusArea')" class="treatChecked" name=${response.PD[i]}></td>
                    <td><input type="checkbox" onclick="excludeCheck('statusArea')" class="fuChecked" name=${response.PD[i]}></td>
                    <td><input type="checkbox" onclick="excludeCheck('statusArea');ambiguous();" class="ambiguousChecked" name=${response.PD[i]}></td>
                    <td><input type="text" class="ambiguousNote"  name=ambiguousNote_${response.PD[i]}></td>
                    <td><input type="checkbox" onclick="excludeCheck('statusArea')" class="pdConfirmed" name=${response.PD[i]}></td>
                    <td><input type="radio" name="deletePatientDisease"><button type="button" onclick="deletelePatientDiseaseRow()" class="btn-close delete deletePatientDisease" aria-label="Close"  data-bs-toggle="modal" data-bs-target="#deletelePatientDiseaseModal"></button></td>
                </tr>
                `)
                $('#statusArea .diagChecked').eq(i).prop('checked',response.diagChecked[i])
                $('#statusArea .treatChecked').eq(i).prop('checked',response.treatChecked[i])
                $('#statusArea .fuChecked').eq(i).prop('checked',response.fuChecked[i])
                $('#statusArea .ambiguousChecked').eq(i).prop('checked',response.ambiguousChecked[i])
                $('#statusArea .ambiguousNote').eq(i).val(response.ambiguousNote[i])
                $('#statusArea .pdConfirmed').eq(i).prop('checked',response.pdConfirmed[i])
                if(response.ambiguousChecked[i]=='true'){
                    $('#statusArea .ambiguousNote').eq(i).prop('disabled',false)
                }else{
                    $('#statusArea .ambiguousNote').eq(i).prop('disabled',true)
                }
                $('#statusArea .diseaseCheck').eq(i).val(response.disease[i])
                $('#statusArea .seqCheck').eq(i).val(response.caSeqNo[i])
            }
            $('#statusArea tbody').append('<tr><td colspan=9><div class="addButton"><button type="button" onclick="addPatientStatus()" class="add btn btn-outline-primary">+</button></div></td></tr>')
        }
    })
}

function addPatientStatus(){
    let chartNo = $('input[name=confirmPID]:checked').next('label').children('.PatientListID').text()
    let seq = ''
    for(let i=0;i<=10;i++){seq+=`<option value=${i}>${i}</option>`}
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:addPatientDiease" %}', // this is the mapping between the url and view
        data:{
            'chartNo':chartNo,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            let PD = response.PD
            $(` <tr data-prepareAdd='true' id=${PD}>
                <td><select onchange="updateDiseaseAndSeq()" class="form-control diseaseCheck">${$('#ChangeDisease').html()}</select></td>
                <td><select onchange="updateDiseaseAndSeq()" class="form-control seqCheck">${seq}</select></td>
                <td><input type="checkbox" onclick="excludeCheck('statusArea')" class="diagChecked" name=${PD}></td>
                <td><input type="checkbox" onclick="excludeCheck('statusArea')" class="treatChecked" name=${PD}></td>
                <td><input type="checkbox" onclick="excludeCheck('statusArea')" class="fuChecked" name=${PD}></td>
                <td><input type="checkbox" onclick="excludeCheck('statusArea');ambiguous();" class="ambiguousChecked" name=${PD}></td>
                <td><input type="text" class="ambiguousNote"  disabled></td>
                <td><input type="checkbox" onclick="excludeCheck('statusArea')" class="pdConfirmed" name=${PD}></td>
                <td><input type="radio" name="deletePatientDisease"><button type="button" onclick="deletelePatientDiseaseRow()" class="btn-close delete deletePatientDisease" aria-label="Close"  data-bs-toggle="modal" data-bs-target="#deletelePatientDiseaseModal"></button></td>
            </tr>
            `).insertBefore($('#statusArea .addButton').parents('tr'))
        }
    })
}
function updateDiseaseAndSeq(){
    let PDID = $(event.target).parents('tr').attr('id')
    let diseaseID = $(event.target).parents('tr').children('td').eq(0).children('select').val()
    let caSeqNo = $(event.target).parents('tr').children('td').eq(1).children('select').val()
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:updateDiseaseAndSeq" %}', // this is the mapping between the url and view
        data:{
            'PDID':PDID,
            'diseaseID':diseaseID,
            'caSeqNo':caSeqNo,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(){
            let caSeqNo = $('#statusArea .seqCheck')
            let caSeqNoObject = '<option value=0>?</option>'
            for(let i=0;i<caSeqNo.length;i++){caSeqNoObject+=`<option value=${caSeqNo.eq(i).val()}>${caSeqNo.eq(i).val()}</option>`}
            let IntervalNoObject = $('.menublock .IntervalNo')
            if(IntervalNoObject.eq(0).html!=undefined){
                IntervalNoObject.map(function(){
                    return $(this).html(caSeqNoObject)
                }).get()
            }
        }
    })
}
function ambiguous(){
    let trID = $(event.target).attr('name')
    if ($(event.target).prop('checked')==true){
        $(event.target).parent('td').next().children('.ambiguousNote').prop('disabled',false)
    }else{
        $(event.target).parent('td').next().children('.ambiguousNote').prop('disabled',true)
    }
}
function excludeCheck(pannel){
    let targetClass=$(event.target).attr('class').split(' ')[0]
    let targetName=$(event.target).attr('name')
    if(targetClass=='pdConfirmed'){
        $(`#${pannel} input[name="${targetName}"][class^="diagChecked"]`).prop('checked',false)
        $(`#${pannel} input[name="${targetName}"][class^="treatChecked"]`).prop('checked',false)
        $(`#${pannel} input[name="${targetName}"][class^="ambiguousChecked"]`).prop('checked',false)
        $(`#${pannel} input[name="${targetName}"][class^="fuChecked"]`).prop('checked',false)
        $(`#${pannel} input[name="ambiguousNote_${targetName}"][class="ambiguousNote"]`).prop('disabled',true)
    }else{
        $(`#${pannel} input[name="${targetName}"][class^="pdConfirmed"]`).prop('checked',false)
    }
}
function patientStatusCheckClose(){
    $('#statusArea .ambiguousNote').val('')
    $("#patientStatusCheck").css('display', 'none');
    
}
function deletelePatientDiseaseRow(){
    $(event.target).prev('input').prop('checked',true)
}
function deletelePatientDisease(){
    let PDID = $('input[name="deletePatientDisease"]:checked').parents('tr').attr('id')
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:deletelePatientDisease" %}', // this is the mapping between the url and view
        data:{
            'PDID':PDID,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            $('input[name="deletePatientDisease"]:checked').parents('tr').remove()
            let caSeqNo = $('#statusArea .seqCheck')
            let caSeqNoObject = '<option value=0>?</option>'
            for(let i=0;i<caSeqNo.length;i++){caSeqNoObject+=`<option value=${caSeqNo.eq(i).val()}>${caSeqNo.eq(i).val()}</option>`}
            let IntervalNoObject = $('.menublock .IntervalNo')
            if(IntervalNoObject.eq(0).html!=undefined){
                IntervalNoObject.map(function(){
                    return $(this).html(caSeqNoObject)
                }).get()
            }
        }
    })
}
function patientStatusSubmit(){
    var target = $('#statusArea').children('table').children('tbody').children('tr[data-prepareAdd="true"]')
    let PD = target.map(function(){return $(this).attr('id')}).get()
    let diagChecked = target.map(function(){return Number($(this).children('td').children('.diagChecked').prop('checked'))}).get()
    let treatChecked = target.map(function(){return Number($(this).children('td').children('.treatChecked').prop('checked'))}).get()
    let fuChecked = target.map(function(){return Number($(this).children('td').children('.fuChecked').prop('checked'))}).get()
    let pdConfirmed = target.map(function(){return Number($(this).children('td').children('.pdConfirmed').prop('checked'))}).get()
    let ambiguousChecked = target.map(function(){return Number($(this).children('td').children('.ambiguousChecked').prop('checked'))}).get()
    let ambiguousNote = target.map(function(){return $(this).children('td').children('.ambiguousNote').val()}).get()
    let total = $('#statusArea .diagChecked').length
    let scrollTop = $('#patient').scrollTop()
    var excludes = 1
    let checked_pdConfirmed = 0
    let checked_diagChecked = 0
    let checked_treatChecked = 0
    let checked_fuChecked = 0
    let checked_ambiguousChecked = 0
    let checked = 0
    for(let i =0;i<pdConfirmed.length;i++){checked_pdConfirmed+=pdConfirmed[i]}
    for(let i =0;i<diagChecked.length;i++){checked_diagChecked+=diagChecked[i]}
    for(let i =0;i<treatChecked.length;i++){checked_treatChecked+=treatChecked[i]}
    for(let i =0;i<fuChecked.length;i++){checked_fuChecked+=fuChecked[i]}
    for(let i =0;i<ambiguousChecked.length;i++){checked_ambiguousChecked+=ambiguousChecked[i]}
    if(checked_pdConfirmed==total||checked_diagChecked==total||checked_treatChecked==total||checked_fuChecked==total||checked_ambiguousChecked==total){
        checked=1
    }
    
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:updatePatientStatus" %}', // this is the mapping between the url and view
        data:{
            'PD':PD,
            'diagChecked':diagChecked,
            'treatChecked':treatChecked,
            'fuChecked':fuChecked,
            'pdConfirmed':pdConfirmed,
            'ambiguousChecked':ambiguousChecked,
            'ambiguousNote':ambiguousNote,
            'scrollTop':scrollTop,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            if($('input[name="disappear"]').is(':checked')==0){
                if(excludes==1){
                    $('input[name=confirmPID]:checked').next('label').css('color','red')
                }else{
                    $('input[name=confirmPID]:checked').next('label').css('color','#FFFFFF')
                }
                if(checked>0){
                    $('input[name=confirmPID]:checked').next('label').css('color','#FFFFFF')
                }else{
                    $('input[name=confirmPID]:checked').next('label').css('color','#AAA')
                }
            }else{
                statusFilter()
            }
            patientStatusCheckClose()
        }
    })
}

function extractedFactorOpen(data_form,procedureID,diseaseId,source){
    let pd = $('input[name="timePID"]:checked').next('label').children('.menu').children('.menublock').eq(0).attr('id').split('_')[3]
    let eventID = $('input[name="timePID"]:checked').next('label').children('.eventID').html()
    let medType= $('input[name="timePID"]:checked').next('label').children('.medType').html()
    let nWindow = $('#extractedFactor').attr('data-window')
    $('#factorGroupArea').empty()
    $("#extractedFactor").css('display', 'inline');
    $("#menu").css('display', 'none');
    $(`#factorGroupArea${data_form} .formStructure`).remove()
    $(`#factorGroupArea${data_form}`).attr('data-eventID',eventID)
    
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:searchExtractedEventFactorCode" %}', // this is the mapping between the url and view
        data:{
            'pd':pd,
            'eventID':eventID,
            'medType':medType,
            'diseaseId':diseaseId,
            'procedureID':procedureID,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            
            $(`.formVersion[data-form=${data_form}]`).empty()
            for(let i=0;i<response.eventFactorCode.length;i++){
                $(`.formVersion[data-form=${data_form}]`).append(`<option value=${response.eventFactorCode[i]}>版本${response.version[i]}</option>`)
            }
            if(source==1){
                for(let j=response.isRecorded.length-1;j>=0;j--){
                    if(response.isRecorded[j]==1){
                        $(`.formVersion[data-form=0]`).children('option').eq(j).prop('selected',true)
                    }
                }
                $(`.formVersion[data-form=1]`).val($(`.formVersion[data-form=0]`).children('option:not(:selected)').eq(0).val())
            }else{
                for(let j=response.isRecorded.length-1;j>=0;j--){
                    if(response.isRecorded[j]==1){
                        $(`.formVersion[data-form=${data_form}]`).children('option').eq(j).prop('selected',true)
                    }
                }
                let eventFactorCode0 = $(`.formVersion[data-form=0]`).val()
                let eventFactorCode1 = $(`.formVersion[data-form=1]`).val()
                if(eventFactorCode0==eventFactorCode1){
                    $(`.formVersion[data-form=${data_form}]`).val($(`.formVersion[data-form=${data_form}]`).children('option:not(:selected)').eq(0).val())
                }
            }
            
            let eventFactorCode = $(`.formVersion[data-form=${data_form}]`).val()
            if(!eventFactorCode==false){
                formGenerator(eventID,eventFactorCode,`#factorGroupArea${data_form}`,'prepend',true,data_form)
                console.log(eventID,eventFactorCode,`#factorGroupArea${data_form}`,'prepend',true,data_form)
            } 
        }
    })
}
    


function changeFormbyDisease(){
    let data_form = $(event.target).attr('data-form')
    let disease = $(event.target).val()
    let procedure = $(event.target).next('.procedureOfForm').val()
    let source = 0 //0=特定的 1=全部
    
    extractedFactorOpen(data_form,procedure,disease,source)
}

function changeForm(){
    let data_form = $(event.target).attr('data-form')
    let eventID = $('input[name="timePID"]:checked').next('label').children('.eventID').html()
    $(`#factorGroupArea${data_form[0]} .formStructure`).remove()
    let eventFactorCode = $(`.formVersion[data-form=${data_form}]`).val()
    let eventFactorCode0 = $(`.formVersion[data-form=0]`).val()
    let eventFactorCode1 = $(`.formVersion[data-form=1]`).val()
    if(eventFactorCode0!=eventFactorCode1){
        formGenerator(eventID,eventFactorCode,`#factorGroupArea${data_form}`,'prepend',true,data_form)
    }
}

function formGenerator(eventID,eventFactorCode,pannel,method,otherFunction,form){
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:formGenerator" %}', // this is the mapping between the url and view
        data:{
            'eventID':eventID,
            'eventFactorCode':eventFactorCode,
            'form':form,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            if(method=='prepend'){
                $(pannel).prepend(response.formObject)
            }else if(method=='append'){
                $(pannel).html(response.formObject)
            }
        },
        complete:function(){
            if(otherFunction==true){
                searchExtractedFactorsRecord(form)
            }
        }
    })
}

function extractedFactorClose(){
    $('#factorGroupArea').empty()
}

function extractedFactorSubmit(form){
    let container = `#factorGroupArea${form}`
    let eventID = $(container).attr('data-eventID')
    //------------------------------------------------------------
    let checkboxIDArray = $(`${container} input[name^="formStructure"][type="checkbox"]:checked`).map(function(){
        return $(this).attr('data-eventFactorID')
    }).get()

    let checkboxValArray = $(`${container} input[name^="formStructure"][type="checkbox"]:checked`).map(function(){
        return $(this).prop('checked')
    }).get()

    let checkboxRecordedArray = $(`${container} input[name^="formStructure"][type="checkbox"]:checked`).map(function(){
        return $(this).attr('data-recorded')
    }).get()
   
    //------------------------------------------------------------
    let radioIDArray = $(`${container} input[name^="formStructure"][type="radio"][data-usage!="text"]:checked`).map(function(){
        return $(this).attr('data-eventFactorID')
    }).get()
    let radioValArray = $(`${container} input[name^="formStructure"][type="radio"][data-usage!="text"]:checked`).map(function(){
        return $(this).prop('checked')
    }).get()

    let radioRecordedArray = $(`${container} input[name^="formStructure"][type="radio"][data-usage!="text"]:checked`).map(function(){
        return $(this).attr('data-recorded')
    }).get()

    //------------------------------------------------------------
    let textIDArray = $(`${container} input[name^="formStructure"][type="text"]`).map(function(){
        if($(this).val()!=''){return $(this).attr('data-eventFactorID')}
    }).get()
    let textValArray = $(`${container} input[name^="formStructure"][type="text"]`).map(function(){
        if($(this).val()!=''){return $(this).val()}
    }).get()

    let textRecordedArray = $(`${container} input[name^="formStructure"][type="text"]`).map(function(){
        if($(this).val()!=''){return $(this).attr('data-recorded')}
    }).get()

    //------------------------------------------------------------
    let dateIDArray = $(`${container} input[name^="formStructure"][type="date"]`).map(function(){
        if($(this).val()!=''){return $(this).attr('data-eventFactorID')}
    }).get()
    let dateValArray = $(`${container} input[name^="formStructure"][type="date"]`).map(function(){
        if($(this).val()!=''){return $(this).val()}
    }).get()

    let dateRecordedArray = $(`${container} input[name^="formStructure"][type="date"]`).map(function(){
        if($(this).val()!=''){return $(this).attr('data-recorded')}
    }).get()

    let version =  $(`.formVersion[data-form=${form}]`).val()
    let procedure =  $(`.procedureOfForm[data-form=${form}]`).val()
    let insertSeq = $(`.procedureOfForm[data-form=${form}]`).children('option:selected').attr('data-seq')
    let insertIDArray =  checkboxIDArray.concat(radioIDArray,textIDArray,dateIDArray)
    let insertValArray = checkboxValArray.concat(radioValArray,textValArray,dateValArray)
    let insertRecordedArray = checkboxRecordedArray.concat(radioRecordedArray,textRecordedArray,dateRecordedArray)

    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:insertExtractedFactors" %}', // this is the mapping between the url and view
        data:{
            'eventID':eventID,
            'procedure':procedure,
            'version':version,
            'insertSeq':insertSeq,
            'insertIDArray':insertIDArray,
            'insertValArray':insertValArray,

            'insertRecordedArray':insertRecordedArray,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(){
            
            Swal.fire({
                title: '',
                html: '儲存成功',
                icon: 'success',
                timer: 1000,
                showConfirmButton: false,
                timerProgressBar: true,
            })
        }
    })

}

function searchExtractedFactorsRecord(form){
    let container = `#factorGroupArea${form}`
    
    //------------------------------------------------------------
    let checkboxIDArray = $('input[name^="formStructure"][type="checkbox"]').map(function(){
        return $(this).attr('data-eventFactorID')
    }).get()

    let checkboxClassArray = $('input[name^="formStructure"][type="checkbox"]').map(function(){
        return $(this).parents('.mainBlock').attr('class').split(' ')[1]
    }).get()

    //------------------------------------------------------------
    let radioIDArray = $('input[name^="formStructure"][type="radio"][data-usage!="text"]').map(function(){
        return $(this).attr('data-eventFactorID')
    }).get()

    let radioClassArray = $('input[name^="formStructure"][type="radio"][data-usage!="text"]').map(function(){
        return $(this).parents('.mainBlock').attr('class').split(' ')[1]
    }).get()

    //------------------------------------------------------------
    let textIDArray = $('input[name^="formStructure"][type="text"]').map(function(){
        return $(this).attr('data-eventFactorID')
    }).get()

    let textClassArray = $('input[name^="formStructure"][type="text"]').map(function(){
        return $(this).parents('.mainBlock').attr('class').split(' ')[1]
    }).get()
    //------------------------------------------------------------
    let dateIDArray = $('input[name^="formStructure"][type="date"]').map(function(){
        return $(this).attr('data-eventFactorID')
    }).get()

    let dateClassArray = $('input[name^="formStructure"][type="date"]').map(function(){
        return $(this).parents('.mainBlock').attr('class').split(' ')[1]
    }).get()

    let eventID = $(container).attr('data-eventID')
    let seq = $(`.procedureOfForm[data-form=${form}]`).children('option:selected').attr('data-seq')
    let diseaseId = $(`.ChangeDisease[data-form=${form}]`).val()
    let idArray =  checkboxIDArray.concat(radioIDArray,textIDArray,dateIDArray)
    let classArray =  checkboxClassArray.concat(radioClassArray,textClassArray,dateClassArray)
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:searchExtractedFactorsRecord" %}', // this is the mapping between the url and view
        data:{
            'eventID':eventID,
            'diseaseId':diseaseId,
            'seq':seq,
            'idArray':idArray,
            'classArray':classArray,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(response){
            
            for(let i=0; i<response.seqRecorded.length; i++){
                let targetObject = $(`.${response.classRecorded[i]} [data-eventFactorID=${response.factorIdRecorded[i]}]`)
                let type = targetObject.attr('type')
                if (type=='text'||type=='date'){
                    targetObject.val(response.factorValueRecorded[i])
                }else{
                    
                    targetObject.prop('checked',response.factorValueRecorded[i])
                }
                targetObject.attr('data-recorded',1)
            }
        }
    })
}

function cancerRegistCheck(){
    $('#checkArea').empty()
    let cloneObject = $('.'+$('input[name="timePID"]:checked').attr('class'))
    for(let i=0; i<cloneObject.length; i++){
        $('#checkArea').append(cloneObject.eq(i).parent().clone(true))
        $('#checkArea input').attr('name','test')
        $('#checkArea .note').remove()
        $('#checkArea .addButton').remove()
        $('#checkArea div').css('width','165px')
        $('#checkArea td').css('height','70px')
        $('#checkArea label').css('height','70px')
        $('#checkArea label').css('width','498px')
        $('#checkArea label').css('margin-left','-12px')
        $('#checkArea label').css('margin-top','0px')
        $('#checkArea .IntervalNo').css('width','55px')
        $('#checkArea .IntervalNo').css('margin','0px')
        $('#checkArea select').css('pointer-events','none')
    }
    $("#cancerRegistCheck").css('display', 'inline');
    $("#menu").css('display', 'none');
}

function cancerRegistCheckClose(){
    $('#checkArea').empty()
    $("#cancerRegistCheck").css('display', 'none');
}

function cancerRegistSubmit(){
    let eventID = $('input[name="test"]:checked').next('label').children('.eventID').html().replaceAll(' ','')
    let EDID = $('input[name="test"]:checked').attr('class').split('sno_')[1]
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:updateCancerRegist" %}', // this is the mapping between the url and view
        data:{
            'EDID':EDID,
            'eventID':eventID,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(){
            $('#timetable #'+$('input[name="test"]').eq(i).attr('id')).next('label').children()
            cancerRegistCheckClose()
        }
    })

    for(let i=0; i<$('input[name="test"]:not(:checked)').length; i++){
        let ob ='#sno_'+EDID+'_'+$('input[name="test"]:not(:checked)').eq(i).next('label').children('.eventID').html().replaceAll(' ','')
        let notCheckedId = $('input[name="test"]:not(:checked)').eq(i).attr('id')
        if($(`#timetable #${notCheckedId}`).next('label').children('.menu').children('.menublock').length==1){
            $(`#timetable #${notCheckedId}`).next('label').children('.menu').children(ob).children('.IntervalNo').val(1)
            $(`#timetable #${notCheckedId}`).next('label').children('.menu').children(ob).children('.phase').val(0)
        }else{
            $(`#timetable #${notCheckedId}`).next('label').children('.menu').children(ob).remove()
        }
    }
    for(let i=0; i<$('input[name="test"]').length; i++){
        let id = $('input[name="test"]').eq(i).attr('id')
        $(`#timetable #${id}`).parent('td').css('background-color','transparent')
        $(`#timetable #${id}`).parent('td').css('color','#000000')
        setdisplay(id.split('timePID')[1])
    }
}

function ascriptionSubmit(){
    let eventID_F = $('#inductionEventID2').text()
    let eventID = $('#inductionEventID1').text()

    if(eventID_F!=''){ //沒歸屬偵測
        $.ajax({
            type: 'post',
            url: '{% url "eventDefinition:updateInducedEvent" %}', // this is the mapping between the url and view
            data:{
                'eventID_F':eventID_F,
                'eventID':eventID,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success:function(){
                
                let eventIDGroup = $('#timetable .eventID').map(function(){return parseInt($(this).html())}).get()
                let index = eventIDGroup.indexOf(parseInt(eventID_F))
                let index_origin = eventIDGroup.indexOf(parseInt(eventID))
                let target = $('#timetable .eventID').eq(index)
                let origin = $('#timetable .eventID').eq(index_origin)
                let num = 0
                if($('.accordion').length==0){
                    num = 0
                }else{
                    num = $('.accordion').length+1
                } 
                let targetID = $('#timetable .eventID').eq(index).parents('label').prevAll('input').attr('id')

                if(target.nextAll('.accordion').length==0){
                    target.parents('label').append(`<div class="btn btn-primary accordion" data-bs-toggle="collapse" data-bs-target="#collapse${num}" ></div>`)
                    target.nextAll('.accordion').css('height',target.parents('label').height()+'px')
                }else{
                    num = parseInt(target.nextAll('.accordion').attr('data-bs-target').split('#collapse')[1])
                }

                

                $(`.collapse${num}`).parents('tr').remove()

                origin.parents('tr').remove()
                addInducedEvent(num,eventID_F,targetID)
            },
            complete:function(){
                ascriptionClose()
            }
        })
    }
}

function deleteEvent_F(){
    let eventID = $(event.target).prevAll('.eventID').html()
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:deleteEvent_F" %}', // this is the mapping between the url and view
        data:{
            'eventID':eventID,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(){
            GetTime()
        }
    })
}

function getNum(){
    let disease = $('#ChangeDisease').val()
    let diagChecked=Number($('#statusFilterPannel .diagChecked').prop('checked'))
    let treatChecked=Number($('#statusFilterPannel .treatChecked').prop('checked'))
    let fuChecked=Number($('#statusFilterPannel .fuChecked').prop('checked'))
    let ambiguousChecked=Number($('#statusFilterPannel .ambiguousChecked').prop('checked'))
    let pdConfirmed=Number($('#statusFilterPannel .pdConfirmed').prop('checked'))
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getNum" %}', // this is the mapping between the url and view
        data:{
            'disease':disease,
            'diagChecked':diagChecked,
            'treatChecked':treatChecked,
            'fuChecked':fuChecked,
            'ambiguousChecked':ambiguousChecked,
            'pdConfirmed':pdConfirmed,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(response){
            let str=['全部']
            $('#filter').children('option').eq(0).html(`${str[0]}(${response.num[0]})`)
        }
    })
}

function move(id){
    var move=false;//移動標記  
    var _x,_y;//左上角位置 
        $(`#${id}`).mousedown(function(e){  
            move=true;  
            _x=e.pageX-parseInt($(`#${id}`).css("left"));  
            _y=e.pageY-parseInt($(`#${id}`).css("top"));       
        });  
        
        $(document).mousemove(function(e){  
            if(move){  
                var x=e.pageX-_x;
                var y=e.pageY-_y;  
                $(`#${id}`).css({"top":y,"left":x}); 
                $(`#${id}`).css({"z-index":2000});
            }  
        }).mouseup(function(){  
            $(`#${id}`).css({"z-index":1030});
            move=false;
    });
}
function  myFunction(){
    if($(event.target).attr('data-checked')==0){
        $(event.target).attr('data-checked','1')
    }else{
        $(event.target).attr('data-checked','0')
        $(event.target).prop('checked',false)
    }
    $('input[name^="formStructure[1]"][type="radio"]:not(:checked)').each(function(){
        $(this).attr('data-checked','0')
    })
}

function addMainBlock(){
    $('#extraFactorMenu').css('display','none')
    var object = $('[data-prepareAdd=1]').clone()
    var objectHTML = object.html()
    var cloneObject = object.find('input[name^="formStructure"]')
    var indexArray = $('input[name^="formStructure"]').map(function(){return parseInt($(this).attr('name').split('_')[1].replaceAll('[','').replaceAll(']',''))}).get()
    var idArray = $('input[name^="formStructure"]').map(function(){return parseInt($(this).attr('id').split('_')[1])}).get()
    var maxIndex = Math.max.apply(Math,indexArray)+1 
    var maxID = Math.max.apply(Math,idArray)
    var names = cloneObject.map(function(){return $(this).attr('name')}).get()
    var id = cloneObject.map(function(){return $(this).attr('id')}).get()
    var subjectID = $('[data-prepareAdd=1]').attr('class').split(' ')[1]
    var dataSeq = Math.max.apply(Math,$(`.${subjectID}`).map(function(){return $(this).attr('data-Seq')}).get())+1 
    for(let i=0;i<names.length;i++){
        var newElement = names[i].split('_')
        var newID = id[i].split('_')
        maxID +=1
        objectHTML = objectHTML.replaceAll(names[i],newElement[0]+`_[${maxIndex}]_`+newElement[2])
        objectHTML = objectHTML.replaceAll(id[i],newID[0]+`_${maxID}`)
    }

    newObject=`<div data-prepareAdd=0 onmousedown="record()" class="mainBlock ${subjectID}" data-Seq=${dataSeq}>`
    newObject+=objectHTML
    newObject+='</div>'
    let className = $('[data-prepareAdd=1]').attr('class').split(' ')[1]
    var dataSeq = Math.max.apply(Math,$(`.${className}`).map(function(){return $(this).attr('data-Seq')}).get())
    $(newObject).insertAfter(`.${className}[data-seq=${dataSeq}]`)
    
}

function record(){
    $('.mainBlock').attr('data-prepareAdd',0)
    $(event.target).children().parents('.mainBlock').attr('data-prepareAdd',1)
    $(event.target).parents('.mainBlock').attr('data-prepareAdd',1)
}

function menu(pannel,menu,useRadio=true){
    if(useRadio){
        $(`#${pannel}`).on('mousedown','td',function(d){
            $(this).children('input[type="radio"]').prop('checked',true)
            showReport()
            if(d.which == 3){  // 1 = 滑鼠左鍵; 2 = 滑鼠中鍵; 3 = 滑鼠右鍵
                
                var x = d.originalEvent.x || d.originalEvent.layerX || 0;
                var y = d.originalEvent.y || d.originalEvent.layerY || 0;
                $(`#${menu}`).css('left', x);
                $(`#${menu}`).css('top', y);
                $(".customMenu").css('display', 'none');
                $(".customMenu").css('z-index', '100');
                $(`#${menu}`).css('display', 'inline');
            }else if(d.which == 1){
                $(".customMenu").css('display', 'none');
            }
            if(menu=="menu"){
                if($('input[name="timePID"]:checked').attr('data-eventCheck')=='True'){
                    $(`#${menu}`).children('#disableEvent').attr('data-eventCheck','0');
                    $(`#${menu}`).children('#disableEvent').html('disabled')
                }else{
                    $(`#${menu}`).children('#disableEvent').attr('data-eventCheck','1');
                    $(`#${menu}`).children('#disableEvent').html('undisabled')
                }
            }
            if(menu=="statusMenu"){
                if($('input[name="confirmPID"]:checked').attr('data-isDone')=='1'){
                    $(`#isDone`).html('標記未完成');
                }else{
                    $(`#isDone`).html('標記已完成');
                }
            }
        })
    }else{
        $(`#${pannel}`).on('mousedown',function(d){
            if(d.which == 3){  // 1 = 滑鼠左鍵; 2 = 滑鼠中鍵; 3 = 滑鼠右鍵
                var x = d.originalEvent.x || d.originalEvent.layerX || 0;
                var y = d.originalEvent.y || d.originalEvent.layerY || 0;
                $(`#${menu}`).css('left', x);
                $(`#${menu}`).css('top', y);
                $(".customMenu").css('display', 'none');
                $(".customMenu").css('z-index', '100');
                $(`#${menu}`).css('display', 'inline');
            }else if(d.which == 1){
                $(".customMenu").css('display', 'none');
            }

        })
    }
}

function statusFilter(){
    $('#Report').empty()
    //let name = $(event.target).attr('name')
    let diagChecked=Number($('#statusFilterPannel .diagChecked').prop('checked'))
    let treatChecked=Number($('#statusFilterPannel .treatChecked').prop('checked'))
    let fuChecked=Number($('#statusFilterPannel .fuChecked').prop('checked'))
    let ambiguousChecked=Number($('#statusFilterPannel .ambiguousChecked').prop('checked'))
    let pdConfirmed=Number($('#statusFilterPannel .pdConfirmed').prop('checked'))
    var disease = $('#ChangeDisease').val()
    let filter = $('#filter').val()
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:confirmpat" %}', // this is the mapping between the url and view
        data:{
            'filter':filter,
            'Disease':disease,
            'diagChecked':diagChecked,
            'treatChecked':treatChecked,
            'fuChecked':fuChecked,
            'ambiguousChecked':ambiguousChecked,
            'pdConfirmed':pdConfirmed,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            $('#Report').append(response.examID) 
            $('#patient').scrollTop(parseInt(response.scrollTop)*1.8616427135304192)
            
            $('input[name="confirmPID"]').map(function(){
                if($(this).attr('data-isDone')=="1"){
                    $(this).next('label').css('color','white')
                }else{
                    $(this).next('label').css('color','red')
                }
            })
        },
        complete:function(){
            if("{{de_identification}}"=='False'){
                $('.ID').css('display','none')
                $('.PatientListID').css('display','inline')
            }else{
                $('.ID').css('display','inline')
                $('.PatientListID').css('display','none')
            }
            $('.loader1').css('display','none')
            $('.PatientListID[data-checked=0]').parents('label').css('color','#AAA')
            getNum()
        }
    })
    
}
function excludeFilter(){
    GetTime()
}
function disableEvent(){
    let eventID = $('input[name=timePID]:checked').next('label').children('.eventID').html()
    let disable = $(event.target).attr('data-eventCheck')
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:updateEventConfirm" %}', // this is the mapping between the url and view
        data:{
            'eventID':eventID,
            'disable':disable,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(){
            let excludeFilter = $('#excludeFilter').is(':checked')
            if(excludeFilter==false){
                $('input[name=timePID]:checked').parents('tr').remove()
            }
            if(disable=='1'){
                $('input[name=timePID]:checked').parents('td').css('background-color','transparent')
            }
            $('#menu').css('display','none')
        }
    })
}
function searchForm(){
    let code = $('input[name="formFilter"]').map(function(){return $(this).val().split('(')[0]}).get()
    if(code.includes('')==false){
        $('#designArea tbody').empty()
        $('#preview').empty()
        $.ajax({
            type: 'post',
            url: '{% url "eventDefinition:searchEventFactorCode" %}', // this is the mapping between the url and view
            data:{
                'groupNo':code[0],
                'diseaseID':code[1],
                'procedureID':code[2],
                'version':code[3],
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success:function(response){
                $('input[list="eventFactorCode"]').val(response.eventFactorCode)
                formGenerator(-999999,response.eventFactorCode,'#preview','append',false)
                getFromStructure(response.eventFactorCode)
            }
        })

    }else{
        $('#designArea tbody').empty()
        $('#preview').empty()
    }
}
function getFromStructure(eventFactorCode){
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getFromStructure" %}', // this is the mapping between the url and view
        data:{
            'eventFactorCode':eventFactorCode,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){

            $('#designArea tbody').empty()
            let object = ''
            for(let i=0;i<response.eventFactorID.length;i++){
                object += '<tr>'
                object += `<td><input onchange="updateStructure()" type='text' class="form-control designFactor eventFactorID" value="${response.eventFactorID[i]}"></td>`
                object += `<td><input onchange="updateStructure()" type='text' class="form-control designFactor serialNo" value="${response.serialNo[i]}"></td>`
                object += `<td><input onchange="updateStructure()" type='text' class="form-control designFactor factorName" value="${response.factorName[i]}"></td>`
                object += `<td><select onchange="updateStructure()" class="form-control designFactor itemType" ><option value="NE">NE</option><option value="text">text</option><option value="radio">radio</option><option value="checkbox">checkbox</option><option value="date">date</option></select></td>`
                object += `<td><select onchange="updateStructure()" class="form-control designFactor labeled" ><option value="true">true</option><option value="false">false</option></select></td>`
                object += `<td><input onchange="updateStructure()" type='text' class="form-control designFactor F_eventFactorID" value="${response.F_eventFactorID[i]}"></td>`
                object += `<td><select onchange="updateStructure()" class="form-control designFactor isLeaf" ><option value="true">true</option><option value="false">false</option></select></td>`
                object += `<td><input type="radio" name="deleteFactorRow"><button type="button" onclick="deleteFactorRow()" class="btn-close delete" aria-label="Close"  data-bs-toggle="modal" data-bs-target="#deleteleModal"></button></td>`
                object += '</tr>'
            }
            object += '<tr><td colspan=8><div class="addButton"><button type="button" onclick="addFactor()" class="add btn btn-outline-primary">+</button></div></td></tr>'
            $('#designArea tbody').html(object)
            for(let j=0;j<response.isLeaf.length;j++){$('.isLeaf').eq(j).val(response.isLeaf[j].toString().replaceAll(' ',''))}
            for(let j=0;j<response.labeled.length;j++){$('.labeled').eq(j).val(response.labeled[j].toString().replaceAll(' ',''))}
            for(let j=0;j<response.itemType.length;j++){$('.itemType').eq(j).val(response.itemType[j].toString().replaceAll(' ',''))}
        }
    })
}
function deleteFactor(){
    $('input[name="deleteFactorRow"]:checked').parents('tr').remove()
    updateStructure()
}
function deleteFactorRow(){
    $(event.target).prev('input').prop('checked',true)
}
function updateStructure(){
    let code = $('.formFilter').map(function(){return $(this).val().split('(')[0]}).get()
    let eventFactorID = $('#designArea .eventFactorID').map(function(){return $(this).val()}).get()
    let eventFactorCode = $('input[list="eventFactorCode"]').val()
    let serialNo = $('#designArea .serialNo').map(function(){return $(this).val()}).get()
    let factorName = $('#designArea .factorName').map(function(){return $(this).val()}).get()
    let itemType = $('#designArea .itemType').map(function(){return $(this).val()}).get()
    let labeled = $('#designArea .labeled').map(function(){return $(this).val()}).get()
    let F_eventFactorID = $('#designArea .F_eventFactorID').map(function(){return $(this).val()}).get()
    let isLeaf = $('#designArea .isLeaf').map(function(){return $(this).val()}).get()
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:updateFromStructure" %}', // this is the mapping between the url and view
        data:{
            'code':code,
            'eventFactorID':eventFactorID,
            'eventFactorCode':eventFactorCode,
            'serialNo':serialNo,
            'factorName':factorName,
            'itemType':itemType,
            'labeled':labeled,
            'F_eventFactorID':F_eventFactorID,
            'isLeaf':isLeaf,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            formGenerator(-999999,code[0],'#preview','append',false)
        }
    })
}
function addFactor(){
    let code = $('.formFilter').map(function(){return $(this).val()}).get()
    let object = ''
    let target = $(event.target)
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getNewEventFactorID" %}', // this is the mapping between the url and view
        data:{
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            if(code.includes('')==false){
                object += '<tr>'
                object += `<td><input onchange="updateStructure()" type='text' class="form-control designFactor eventFactorID" value="${response.newEventFactorID}"></td>`
                object += `<td><input onchange="updateStructure()" type='text' class="form-control designFactor serialNo" value=""></td>`
                object += `<td><input onchange="updateStructure()" type='text' class="form-control designFactor factorName" value=""></td>`
                object += `<td><select onchange="updateStructure()" class="form-control designFactor itemType" ><option value="NE">NE</option><option value="text">text</option><option value="radio">radio</option><option value="checkbox">checkbox</option><option value="date">date</option></select></td>`
                object += `<td><select onchange="updateStructure()" class="form-control designFactor labeled" ><option value="true">true</option><option value="false">false</option></select></td>`
                object += `<td><input onchange="updateStructure()" type='text' class="form-control designFactor F_eventFactorID" value=""></td>`
                object += `<td><select onchange="updateStructure()" class="form-control designFactor isLeaf" ><option value="true">true</option><option value="false">false</option></select></td>`
                object += `<td><input type="radio" name="deleteFactorRow"><button type="button" onclick="deleteFactorRow()" class="btn-close delete" aria-label="Close"  data-bs-toggle="modal" data-bs-target="#deleteleModal"></button></td>`
                object += '</tr>'
                target.parents('tr').before(object)
                updateStructure()
            }
        }
    })
}
function formDesign(){
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getEventFactorCode" %}', // this is the mapping between the url and view
        data:{
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            //formGenerator(-999999,code[0],'#preview','append','')
            $('#formFilter #eventFactorCode').empty()
            $('#formFilter #groupNo').empty()
            $('#formFilter #diseaseID').empty()
            $('#formFilter #procedureID').empty()
            $('#formFilter #version').empty()
            for(let i=0;i<response.eventFactorCode.length;i++){$('#formFilter #eventFactorCode').append(`<option value="${response.eventFactorCode[i]}">`)}
            for(let i=0;i<response.groupNo.length;i++){$('#formFilter #groupNo').append(`<option value="${response.groupNo[i]}">`)}
            for(let i=0;i<response.diseaseID.length;i++){$('#formFilter #diseaseID').append(`<option value="${response.diseaseID[i]}(${response.disease[i].replaceAll(' ','')})">`)}
            for(let i=0;i<response.procedureID.length;i++){$('#formFilter #procedureID').append(`<option value="${response.procedureID[i]}(${response.procedureName[i].replaceAll(' ','')})">`)}
            for(let i=0;i<response.version.length;i++){$('#formFilter #version').append(`<option value="${response.version[i]}">`)}
        }
    })
    $("#formDesignPannel").css('display', 'inline');
    $("#menu").css('display', 'none');
    $("#statusMenu").css('display', 'none');
}
function formDesignClose(){
    $(".formFilter").val('')
    $("#preview").empty()
    $("#designArea tbody").empty()
    $("#formDesignPannel").css('display', 'none');
}

function updateEventNote(){
    let eventID = $(event.target).parent('.note').prevAll('.eventID').html()
    let note = $(event.target).val()
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:updateEventNote" %}', // this is the mapping between the url and view
        data:{
            'eventID':eventID,
            'note':note,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        }
    })
}

function emptyAll(){
    $('#extractedFactor #factorGroupArea .formStructure').find('input[type="checkbox"]').prop('checked',false)
    $('#extractedFactor #factorGroupArea .formStructure').find('input[type="radio"]').prop('checked',false)
    $('#extractedFactor #factorGroupArea .formStructure').find('input[type="text"]').val('')
    $('#extractFactorMenu').css('display','none')
}

function isDone(){
    let chartNo = $('input[name="confirmPID"]:checked').next('label').children('.PatientListID').text()
    let isDone = $('input[name="confirmPID"]:checked').attr('data-isDone')
    if(isDone=="1"){
        $('input[name="confirmPID"]:checked').attr('data-isDone','0')
        $('input[name="confirmPID"]:checked').next('label').css('color','red')
    }else{
        $('input[name="confirmPID"]:checked').attr('data-isDone','1')
        $('input[name="confirmPID"]:checked').next('label').css('color','white')
    }
    isDone = $('input[name="confirmPID"]:checked').attr('data-isDone')
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:isDone" %}', // this is the mapping between the url and view
        data:{
            'isDone':isDone,
            'chartNo':chartNo,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(response){
            $('#statusMenu').css('display','none')
        }
    })
}

function getCurrentEventProcedure(){
    let optionName = $('input[name="timePID"]:checked').next('label').children('.menu').children('.menublock').map(function(){return $(this).children('.phase').children('option:checked').html()}).get()
    let optionValue = $('input[name="timePID"]:checked').next('label').children('.menu').children('.menublock').map(function(){return $(this).children('.phase').children('option:checked').val()}).get()
    $('.procedureOfForm').empty()

    $('.procedureOfForm').map(function(){
        for(let i=0;i<optionName.length;i++){
            $(this).append(`<option data-seq=${i+1} value=${optionValue[i]}>${i+1}.${optionName[i]}</option>`)
        }  
    },optionName,optionValue)

    let procedureID = $('.procedureOfForm').map(function(){return $(this).val()}).get()
    let diseaseId = $('.formDisease').map(function(){return $(this).val()}).get()
    let data_form = [0,1]
    let source = 1 //0=特定的 1=全部
    for(let j=0;j<data_form.length;j++){
        extractedFactorOpen(data_form[j],procedureID[j],diseaseId[j],source);
    }
    
}   

function procedureOfForm(){
    let data_form = [$(event.target).attr('data-form')]
    let procedure = $(event.target).val()
    let disease = $(event.target).prev('.formDisease').val()
    let source = 0 //0=特定的 1=全部
    extractedFactorOpen(data_form,procedure,disease,source)
}

function addTopicFormOpen(){
    let disease = $('#ChangeDisease').val()
    $('#addTopicForm').css('display','inline')
    $('#statusMenu').css('display','none')
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getTopic" %}', // this is the mapping between the url and view
        data:{
            'disease':disease,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(response){
            $('#topicArea').empty()
            for(let i=0;i<response.topic.length;i++){
                $('#topicArea').append(`
                    <div class="form-check">
                    <input class="form-check-input" type="checkbox" name="topic" data-Annotated=0 data-topicNo="${response.topicNo[i]}" data-diseaseID="${response.diseaseID[i]}" id="topic_${response.topicNo[i]}">
                    <label class="form-check-label" for="topic_${response.topicNo[i]}">${response.topic[i]}</label>
                    </div>
                    `)
            }
        },
        complete:function(){
            addTopicFormRecord()
        }
    })
}
function addTopicFormRecord(){
    let chartNo = $('input[name="confirmPID"]:checked').next('label').children('.PatientListID').text()
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getTopicRecord" %}', // this is the mapping between the url and view
        data:{
            'chartNo':chartNo,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function(response){
            $('input[name="topic"]').prop('checked',false)
            for(let i=0;i<response.topicNo.length;i++){
                $(`input[name="topic"][data-topicNo="${response.topicNo[i]}"]`).prop('checked',true)
                $(`input[name="topic"][data-topicNo="${response.topicNo[i]}"]`).attr('data-Annotated',1)
            }
        }
    })
}


function addTopicFormClose(){
    $('#addTopicForm').css('display','none')
}

function addTopicFormSubmit(){
    let chartNo = $('input[name="confirmPID"]:checked').next('label').children('.PatientListID').text()

    let topicNo = $(`input[name="topic"]`).map(function(){
        return $(this).attr('data-topicNo')
    }).get()
    let diseaseID = $(`input[name="topic"]`).map(function(){
        return $(this).attr('data-diseaseID')
    }).get()
    let annotated = $(`input[name="topic"]`).map(function(){
        return $(this).attr('data-Annotated')
    }).get()
    let checked = $(`input[name="topic"]`).map(function(){
        return Number($(this).is(':checked'))
    }).get()
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:processCorrelationPatientListAndAnnotation" %}', // this is the mapping between the url and view
        data:{
            'chartNo':chartNo,
            'topicNo':topicNo,
            'diseaseID':diseaseID,
            'annotated':annotated,
            'checked':checked,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            addTopicFormClose()
            Swal.fire({
                title: '',
                html: '儲存成功',
                icon: 'success',
                timer: 1000,
                showConfirmButton: false,
                timerProgressBar: true,
            })
        }
    })
}

function getTopicPatientNum(){
    let disease = $('#ChangeDisease').val()
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:getTopicPatientNum" %}', // this is the mapping between the url and view
        data:{
            'disease':disease,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            $('#filter option:not(:first-child)').remove()
            for(var i=0;i<response.topic.length;i++){
                $('#filter').append(`<option value=${response.topicNo[i]}>${response.topic[i]}(${response.num[i]})</option>`)
            }
        }
    })
}

function onewindow(){
    let width = $('#extractedFactor').width()
    let nWindow = $('#extractedFactor').attr('data-window')
    let select = $('#extractedFactor .ascriptionHeader .form-select').map(function(){return $(this).css('width')}).get()
    if(nWindow==2){
        $('#extractedFactor').css('width',`calc(45.5% - 200px)`)
        $('#extractedFactor').attr('data-window',1)
        
    }
    $('#extractedFactor2').css('display','none')
    $('#extractFactorMenu').css('display','none')
}

function twowindow(){
    let width = $('#extractedFactor').width()
    let nWindow = $('#extractedFactor').attr('data-window')
    let select = $('#extractedFactor .ascriptionHeader .form-select').map(function(){return $(this).css('width')}).get()
    let half = 45.5/2 
    if(nWindow==1){
        $('#extractedFactor').css('width',`calc(${half}% - 100px)`)
        $('#extractedFactor').attr('data-window',2)
        
    }
    $('#extractedFactor2').css('display','inline')
    $('#extractFactorMenu').css('display','none')
}

$(document).ready(function (e) {
    
    $('#defaultMenuBlock1').get(0).oncontextmenu = function() {
        return false
    };

    $('#defaultMenuBlock2','body').get(0).oncontextmenu = function() {
        return false
    };
    //右鍵選單
    menu('defaultMenuBlock1','statusMenu')
    menu('defaultMenuBlock2','menu')
    menu('extractedFactor','extractFactorMenu',false)
    menu('extractedFactor2','extractFactorMenu',false)
    move('ascription')
    move('cancerRegistCheck')
    move('patientStatusCheck')
    move('addTopicForm')
    move('formDesignPannel')
    


    $('.loader1').css('display','inline')
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:Disease" %}', // this is the mapping between the url and view
        data:{
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            for(var i=0;i<response.DiseaseNo.length;i++){
                $('#Disease').children('#ChangeDisease').append(`<option value=${response.DiseaseNo[i]}>${response.Disease[i]}</option>`)
                $('.formDisease').append(`<option value=${response.DiseaseNo[i]}>${response.Disease[i]}</option>`)
            }
        },
        complete:function (){
            statusFilter()
            getTopicPatientNum()
        }
    })


    selection ='<option value="0">請選擇階段</option>'
    $.ajax({
        type: 'post',
        url: '{% url "eventDefinition:Phase" %}', // this is the mapping between the url and view
        data:{
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success:function (response){
            selection += response.phase
        }
    })
    
    $('#ChangeDisease').on('change',function (){
        ascriptionClose(detect=true)
        cancerRegistCheckClose()
        patientStatusCheckClose()
        extractedFactorClose()
        addTopicFormClose()
        $('#accordionExample').empty()
        let filter = $('#filter').val()
        let disease = $('#ChangeDisease').val()
        $('.formDisease').val(disease)
        $('.factorGroupArea').empty()
        $('.procedureOfForm').empty()
        $('.formVersion').empty()
        $('#Report').empty()
        statusFilter()
        getTopicPatientNum()
        $('#statusFilterPannel').css('display','inline')
    })
    $('#filter').on('change',function (){
        ascriptionClose(detect=true)
        cancerRegistCheckClose()
        patientStatusCheckClose()
        extractedFactorClose()
        addTopicFormClose()
        $('#accordionExample').empty()
        let filter = $('#filter').val()
        let disease = $('#ChangeDisease').val()
        $('#Report').empty()
        statusFilter()
        if(filter!=0){
            $('#statusFilterPannel').css('display','none')
        }else{
            $('#statusFilterPannel').css('display','inline')
        }
    })
    
})

