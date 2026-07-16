class ReportType(int):
    other = 100
    violence = 101
    spam = 102
    pornography = 103
    child_abuse = 104
    copyright = 105
    phishing = 106

class ChatAction(str):
    typing = "Typing"
    uploading = "Uploading"
    recording = "Recording"

class VoiceChatState(str):
    mute = "Mute"
    unmute = "Unmute"
    request_speak = 'RequestSpeak'
    cancel_request_speak = 'CancelRequestSpeak'

class GroupAdminAccess(str):
    set_admin = "SetAdmin"
    ban_member = "BanMember"
    change_info = "ChangeInfo"
    pin_message = "PinMessages"
    set_join_link = "SetJoinLink"
    set_member_access = "SetMemberAccess"
    delete_message = "DeleteGlobalAllMessages"
    delete_global_all_messages = "DeleteGlobalAllMessages"

class ChannelAdminAccess(str):
    set_admin = "SetAdmin"    
    add_member = "AddMember"
    view_admins = "ViewAdmins"
    change_info = "ChangeInfo"
    pin_message = "PinMessages"
    view_members = "ViewMembers"
    set_join_link = "SetJoinLink"
    send_message = "SendMessages"
    edit_message = "EditAllMessages"
    delete_message = "DeleteGlobalAllMessages"
    delete_global_all_messages = "DeleteGlobalAllMessages"

class GroupDefaultAccess(str):
    add_member = "AddMember"
    view_admins = "ViewAdmins"
    view_members = "ViewMembers"
    send_message = "SendMessages"

class MessageType(str):
    me = "me"
    gif = "gif"
    self = "me"
    poll = "poll"
    file = "file"
    text = "text"
    live = "live"
    myself = "me"
    bots = "bots"
    users = "users"
    event = "event"
    voice = "voice"
    image = "image"
    photo = "image"
    video = "video"
    music = "music"
    edited = "edited"
    sticker = "sticker"
    contact = "contact"
    location = "location"
    forwarded = "forwarded"

class CallDiscardReason(str):
    missed = "Missed"
    disconnect = "Disconnect"

class AskSpamType(str):
    cancel = "Cancel"
    block_user = "BlockUser"
    add_to_contact = "AddToContact"
    report_and_leave = "ReportAndLeave"

class DeleteMessageType(str):
    local = "Local"
    globall = "Global"
    scheduled = "Scheduled"

class FilterMessageType(str):
    gif = "Gif"
    file = "File"
    link = "Link"
    voice = "Voice"
    music = "Music"
    media = "Media"