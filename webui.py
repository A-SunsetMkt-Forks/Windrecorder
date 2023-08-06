import streamlit as st
import dbManager
import os
import maintainManager
import time
import json
import utils
import datetime
from collections import OrderedDict
import subprocess

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
lang_map = d_lang['lang_map']

# 获取配置中语言选项是第几位；使设置选择项能匹配
def get_language_index(lang,data):
  for i, l in enumerate(data):
    if l == lang:
      return i
  return 1

lang_index = get_language_index(lang,d_lang)



st.set_page_config(
     page_title="Windrecorder",
     page_icon="🦝",
     layout="wide"
)

dbManager.db_main_initialize()


# 将数据库的视频名加上-OCRED标志，使之能正常读取到
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
    select_num = 0

    if is_df_result_exist == 1:
        # 如果结果只有一个，直接显示结果而不显示滑杆
        return 0
    elif not is_df_result_exist == 0:
        # shape是一个元组,索引0对应行数,索引1对应列数。
        total_raw = df.shape[0]
        print("total_raw:" + str(total_raw))

        # 使用滑杆选择视频
        col1,col2 = st.columns([5,1])
        with col1:
            select_num = st.slider(d_lang[lang]["def_search_slider"], 0, total_raw - 1,select_num)
        with col2:
            select_num = st.number_input(d_lang[lang]["def_search_slider"],label_visibility="hidden",min_value=0,max_value=total_raw - 1,value=select_num)
    
        return select_num
    else:
        return 0


# 对搜索结果执行翻页查询
def db_set_page(btn,page_index):
    if btn == "L":
        if page_index <= 0:
            return 0
        else:
            page_index -= 1
            return page_index
    elif btn == "R":
        page_index += 1
        return page_index



# 数据库的前置索引状态提示
def web_db_state_info_before():
    count, nocred_count = web_db_check_folder_marked_file(video_path)
    if nocred_count>0:
        st.warning(d_lang[lang]["tab_setting_db_state1"].format(nocred_count=nocred_count,count=count),icon='🧭')
        return True
    else:
        st.success(d_lang[lang]["tab_setting_db_state2"].format(nocred_count=nocred_count,count=count),icon='✅')
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
def config_set_lang(lang_name):
    INVERTED_LANG_MAP = {v: k for k, v in lang_map.items()}
    lang_code = INVERTED_LANG_MAP.get(lang_name)
    
    if not lang_code:
        print(f"Invalid language name: {lang_name}")
        return

    with open('config.json') as f:
        config = json.load(f)

    config['lang'] = lang_code

    with open('config.json', 'w') as f:
        json.dump(config, f)


# 更改config文件项目
def config_set(name,value):
    with open('config.json') as f:
        config = json.load(f)

    config[name] = value

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
    # st.markdown(f'Database latest record time: **{latest_record_time_str}**, Database records: **{latest_db_records}**, Video Files on disk: **{videos_file_size} GB**')
    st.markdown(d_lang[lang]["footer_info"].format(latest_record_time_str=latest_record_time_str,latest_db_records=latest_db_records,videos_file_size=videos_file_size))








# 主界面_________________________________________________________
st.markdown(d_lang[lang]["main_title"])


tab1, tab2, tab3 = st.tabs([d_lang[lang]["tab_name_search"], d_lang[lang]["tab_name_recording"], d_lang[lang]["tab_name_setting"]])

with tab1:

    
    col1,col2 = st.columns([1,2])
    with col1:
        st.markdown(d_lang[lang]["tab_search_title"])

        col1a,col2a,col3a = st.columns([3,2,1])
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
        with col3a:
            # 翻页
            page_index = st.number_input("搜索结果页数",min_value=0,step=1)



        # 获取数据
        df = dbManager.db_search_data(db_filepath,search_content,search_date_range_in,search_date_range_out,page_index)
        df = dbManager.db_refine_search_data(df)
        is_df_result_exist = len(df)

        # 滑杆选择
        result_choose_num = choose_search_result_num(df,is_df_result_exist)

        if len(df) == 0:
            st.write(d_lang[lang]["tab_search_word_no"].format(search_content=search_content))

        else:
            # 打表
            st.dataframe(
                df,
                column_config={
                    "is_videofile_exist": st.column_config.CheckboxColumn(
                    "is_videofile_exist",
                    help=d_lang[lang]["tab_search_table_help1"],
                    default=False,
                    ),
                    "ocr_text": st.column_config.TextColumn(
                    "ocr_text",
                    help=d_lang[lang]["tab_search_table_help2"],
                    width="large"
                    ),
                    "thumbnail": st.column_config.ImageColumn(
                    "thumbnail", 
                    help=d_lang[lang]["tab_search_table_help3"]
                    )

                },
                height = 800
            )



    with col2:
        # 选择视频
        show_n_locate_video_timestamp(df,result_choose_num)




with tab2:
    st.markdown(d_lang[lang]["tab_record_title"])

    col1c,col2c = st.columns([1,3])
    with col1c:
        st.write("WIP")
        st.success("正在持续录制屏幕……",icon="🦚")
        st.error("录制服务未启用。当前未在录制屏幕。",icon="🦫")
        st.warning("录制服务已启用。当前暂停录制屏幕。",icon="🦫")
        st.button('开始持续录制',type="primary")
        st.button('停止录制屏幕',type="secondary")
        st.checkbox('开机后自动开始录制',value=False)
        st.checkbox('当鼠标一段时间没有移动时暂停录制，直到鼠标开始移动',value=False)
        st.number_input('鼠标停止移动的第几分钟暂停录制',value=5,min_value=1)
    
    with col2c:
        st.write("WIP")



def update_database_clicked():
    st.session_state.update_button_disabled = True

with tab3:
    st.markdown(d_lang[lang]["tab_setting_title"])

    col1b,col2b = st.columns([1,3])
    with col1b:
        # 更新数据库
        st.markdown(d_lang[lang]["tab_setting_db_title"])
        need_to_update_db = web_db_state_info_before()

        col1,col2 = st.columns([1,1])
        with col1:
            update_db_btn = st.button(d_lang[lang]["tab_setting_db_btn"], type="primary", key='update_button_key', disabled=st.session_state.get("update_button_disabled", False), on_click=update_database_clicked)
            is_shutdown_pasocon_after_updatedDB = st.checkbox('更新完毕后关闭计算机',value=False)

            if update_db_btn:
                try:
                    with st.spinner(d_lang[lang]["tab_setting_db_tip1"]):
                        timeCost=time.time()
                        # todo 给出预估剩余时间
                        maintainManager.maintain_manager_main()

                        timeCost=time.time() - timeCost
                except Exception as ex:
                    st.exception(ex)
                    # st.write(f'Something went wrong!: {ex}')
                else:
                    st.write(d_lang[lang]["tab_setting_db_tip3"].format(timeCost=timeCost))
                finally:
                    if is_shutdown_pasocon_after_updatedDB:
                        subprocess.run(["shutdown", "-s", "-t", "60"], shell=True)
                    st.snow()
                    st.session_state.update_button_disabled = False
                    st.button(d_lang[lang]["tab_setting_db_btn_gotit"], key=reset_button_key)
        with col2:
            if config["ocr_engine"] == "Windows.Media.Ocr.Cli":
                config_ocr_engine_choice_index = 0
            elif config["ocr_engine"] == "ChineseOCR_lite_onnx":
                config_ocr_engine_choice_index = 1
            config_ocr_engine = st.selectbox('本地 OCR 引擎',('Windows.Media.Ocr.Cli','ChineseOCR_lite_onnx'),index=config_ocr_engine_choice_index)
            
        


        st.divider()

        # 自动化维护选项 WIP
        st.markdown(d_lang[lang]["tab_setting_maintain_title"])
        st.selectbox('OCR 索引策略',
             ('计算机空闲时自动索引','每录制完一个视频切片就自动更新一次','不自动更新，仅手动更新')
             )
        config_vid_store_day = st.number_input(d_lang[lang]["tab_setting_m_vid_store_time"],min_value=1,value=90)


        st.divider()

        # 选择语言
        st.markdown(d_lang[lang]["tab_setting_ui_title"])

        config_max_search_result_num = st.number_input(d_lang[lang]["tab_setting_ui_result_num"],min_value=1,max_value=500,value=config["max_page_result"])
        
        lang_choice = OrderedDict((k, ''+v) for k,v in lang_map.items())
        language_option = st.selectbox(
            'Interface Language / 更改显示语言',
            (list(lang_choice.values())),
            index=lang_index)
        

        st.divider()

        if st.button('Apple All Change / 应用所有更改',type="primary"):
            config_set_lang(language_option)
            config_set("max_page_result",config_max_search_result_num)
            config_set("ocr_engine",config_ocr_engine)
            st.toast("已应用更改。",icon="🦝")
            st.experimental_rerun()
    


    with col2b:
        st.write("WIP")



web_footer_state()
