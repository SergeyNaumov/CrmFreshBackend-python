def phone_abonent_filter_code(form,field,row):
    form.pre(row)
    return row['a__phone']

def duration_filter_code(form, field, row):
    result=row['wt__duration']
    if row['wt__download_link']:
        audio=f"""
        <div style='padding-top: 5px'>
            <audio controls>
              <source src="{row['wt__download_link']}" type="audio/ogg">
              <source src="{row['wt__download_link']}" type="audio/mpeg">
            Your browser does not support the audio element.
            </audio>
        </div>
        """
        result=str(result)+str(audio)

    return result

events={
    'duration':{
        'filter_code':duration_filter_code
    },
    'phone_abonent':{
        'filter_code':phone_abonent_filter_code
    }
}