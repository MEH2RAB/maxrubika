from .add_folder import AddFolder
from .delete_folder import DeleteFolder
from .edit_folder import EditFolder
from .get_folders import GetFolders
from .get_suggested_folders import GetSuggestedFolders
from .reorder_folder import ReorderFolder

class Folders(
    AddFolder,
    DeleteFolder,
    EditFolder,
    GetFolders,
    GetSuggestedFolders,
    ReorderFolder
):
    pass