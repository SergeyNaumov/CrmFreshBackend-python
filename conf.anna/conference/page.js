window.conference_go_link_lock=false
window.conference_go_link=(link)=>{
    //console.log('href:',link.getAttribute('href'))
    //console.log('id:',link.getAttribute('data-id'))
    if(window.conference_go_link_lock){
        return true
    }
    window.conference_go_link_lock=true
    

    window.app.$http.get(
        BackendBase+'/anna/conference_stat/'+link.getAttribute('data-id')
    ).then(
        r=>{
            let d=r.data
            if(d.success){
                
            }
            setTimeout(
                ()=>{
                    window.conference_go_link_lock=false
                    //console.log('stat false')
                },
                10000

            )

            window.open(link.getAttribute('href'));
        }
    )
    return false
}