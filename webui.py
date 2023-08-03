import streamlit as st
import dbManager
import os
import maintainManager
import time
import json
import utils
import datetime

update_button_key = "update_button"
reset_button_key = "setting_reset"


# python -m streamlit run webui.py
with open('config.json') as f:
    config = json.load(f)
print("config.json:")
print(config)

db_path = config["db_path"]
db_filename = config["db_filename"]
db_filepath = db_path +"/"+ db_filename
video_path = config["record_videos_dir"]
lang = config["lang"]

with open("languages.json", encoding='utf-8') as f:
    d_lang = json.load(f)


st.set_page_config(
     page_title="Windrecorder",
     page_icon="🦝",
     layout="wide"
)

dbManager.db_main_initialize()


# 将数据库的视频名加上OCRED标志，使之能正常读取到
def combine_vid_name_withOCR(video_name):
    vidname = os.path.splitext(video_name)[0] + "-OCRED" + os.path.splitext(video_name)[1]
    return vidname


# 定位视频时间码，展示视频
def show_n_locate_video_timestamp(df,num):
    if is_df_result_exist:
        # todo 获取有多少行结果 对num进行合法性判断
        # todo 判断视频需要存在才能播放
        videofile_path = os.path.join(video_path,combine_vid_name_withOCR(df.iloc[num]['videofile_name']))
        print("videofile_path: "+videofile_path)
        vid_timestamp = calc_vid_inside_time(df,num)
        print("vid_timestamp: "+str(vid_timestamp))
    
        st.session_state.vid_vid_timestamp = 0
        st.session_state.vid_vid_timestamp = vid_timestamp
        # st.session_state.vid_vid_timestamp
        # 判断视频文件是否存在
        if os.path.isfile(videofile_path):
            video_file = open(videofile_path, 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes, start_time=st.session_state.vid_vid_timestamp)
        else:
            st.markdown(f"Video File **{videofile_path}** not on disk.")


# 计算视频对应时间戳
def calc_vid_inside_time(df,num):
    fulltime = df.iloc[num]['videofile_time']
    vidfilename = os.path.splitext(df.iloc[num]['videofile_name'])[0]
    vid_timestamp = fulltime - dbManager.date_to_seconds(vidfilename)
    print("fulltime:"+str(fulltime)+"\n vidfilename:"+str(vidfilename)+"\n vid_timestamp:"+str(vid_timestamp))
    return vid_timestamp


# 选择播放视频的行数 的滑杆组件
def choose_search_result_num(df,is_df_result_exist):
    if not is_df_result_exist == 0:
        # shape是一个元组,索引0对应行数,索引1对应列数。
        total_raw = df.shape[0]
        print("total_raw:" + str(total_raw))
        select_num = st.slider('Rewind Video', 0, total_raw - 1,0)
        return select_num
    else:
        return 0


# 数据库的前置索引状态提示
def web_db_state_info_before():
    count, nocred_count = web_db_check_folder_marked_file(video_path)
    if nocred_count>0:
        st.warning(f' {nocred_count} Video Files need to index. ({count} files total on disk.)',icon='🧭')
        return True
    else:
        st.success(f'No Video Files need to index. ({count} files total on disk.)',icon='✅')
        return False


# 检查 videos 文件夹内有无以"-OCRED"结尾的视频
def web_db_check_folder_marked_file(folder_path):
    count = 0   
    nocred_count = 0   
    for filename in os.listdir(folder_path):
        count += 1
        if not filename.split('.')[0].endswith("-OCRED"):
            nocred_count += 1       
    return count, nocred_count


# 更改语言
def config_set_lang(lang):
    with open('config.json') as f:
        config = json.load(f)
    
    if lang == "English":
        config['lang'] = "en"
    elif lang == "简体中文":
        config['lang'] = "zh"
    
    with open('config.json', 'w') as f:
        json.dump(config, f) 
    
    



# footer状态信息
def web_footer_state():
    latest_record_time_int = dbManager.db_latest_record_time(db_filepath)
    latest_record_time_str = dbManager.seconds_to_date(latest_record_time_int)

    latest_db_records = dbManager.db_num_records(db_filepath)

    videos_file_size = round(utils.get_dir_size(video_path)/(1024*1024*1024),3)

    # webUI draw
    st.divider()
    st.markdown(f'Database latest record time: **{latest_record_time_str}**, Database records: **{latest_db_records}**, Video Files on disk: **{videos_file_size} GB**')








# 主界面_________________________________________________________
st.markdown(d_lang[lang]["main_title"])



tab1, tab2, tab3 = st.tabs([d_lang[lang]["tab_name_search"], d_lang[lang]["tab_name_recording"], d_lang[lang]["tab_name_setting"]])

with tab1:

    
    col1,col2 = st.columns([1,2])
    with col1:
        st.markdown(d_lang[lang]["tab_search_title"])

        col1a,col2a = st.columns([3,2])
        with col1a:
            search_content = st.text_input(d_lang[lang]["tab_search_compname"], 'Hello')
        with col2a:
            # 时间搜索范围组件
            latest_record_time_int = dbManager.db_latest_record_time(db_filepath)
            search_date_range_in, search_date_range_out=st.date_input(
                d_lang[lang]["tab_search_daterange"],
                (datetime.datetime(2000, 1, 1) + datetime.timedelta(seconds=latest_record_time_int) - datetime.timedelta(seconds=86400), datetime.datetime.now()),
                format="YYYY-MM-DD"
                )

        # search_cb = st.checkbox('Searching',value=True)


        # if search_cb:

        # 获取数据
        df = dbManager.db_search_data(db_filepath,search_content,search_date_range_in,search_date_range_out)
        df = dbManager.db_refine_search_data(df)
        is_df_result_exist = len(df)

        # 滑杆选择
        result_choose_num = choose_search_result_num(df,is_df_result_exist)

        if len(df) == 0:
            st.write(d_lang[lang]["tab_search_word_no"].format(search_content=search_content))

        else:
            # st.write('Result about '+search_content)
            # 打表
            st.dataframe(
                df,
                column_config={
                    "is_videofile_exist": st.column_config.CheckboxColumn(
                    "is_videofile_exist",
                    help="Is video file existed?",
                    default=False,
                    ),

                    "ocr_text": st.column_config.TextColumn(
                    "ocr_text",
                    help="Something I found!🎈",
                    width="large"
                    ),

                    "thumbnail": st.column_config.ImageColumn(
                    "thumbnail", help="timestamp preview screenshots"
                    )

                },
                height = 700
            )

    with col2:
        # 选择视频
        show_n_locate_video_timestamp(df,result_choose_num)


    
    web_footer_state()



def update_database_clicked():
    st.session_state.update_button_disabled = True

with tab2:
    st.markdown("## Recording State")

with tab3:
    st.markdown("## Setting")

    col1b,col2b = st.columns([1,3])
    with col1b:
        # 更新数据库
        st.markdown("### Datebase\n")
        need_to_update_db = web_db_state_info_before()
        if st.button('Update Database', type="primary", key='update_button_key', disabled=st.session_state.get("update_button_disabled", False), on_click=update_database_clicked):
            try:
                with st.spinner("Updating Database... You can see process on terminal. Estimated time:"):
                    timeCost=time.time()
                    # todo 给出预估剩余时间
                    maintainManager.maintain_manager_main()

                    timeCost=time.time() - timeCost
            except Exception as ex:
                st.write(f'Something went wrong!: {ex}')
            else:
                st.write(f'Database Updated! Time cost: {timeCost}s')
            finally:
                st.snow()
                st.session_state.update_button_disabled = False
                st.button('Got it.', key=reset_button_key)

        st.divider()

        # 选择语言
        st.markdown("### Interface\n")
        language_option = st.selectbox(
            'Interface Language / 更改界面显示语言',
            ('English', '简体中文'))
        config_set_lang(language_option)
        st.button('Update Language',type="secondary")
    


    with col2b:
        print("col2b")




