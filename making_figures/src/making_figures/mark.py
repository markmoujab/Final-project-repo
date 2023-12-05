from datafed.CommandLib import API
df_api = API()
pl_resp = df_api.projectList()
print(pl_resp)
print(type(pl_resp), len(pl_resp))
type(pl_resp[0])
print(df_api.getContext())
print(df_api.collectionView("root", context="u/markmoujabber"))
print(df_api.collectionView("root"))

ls_resp = df_api.collectionItemsList("root", context="u/markmoujabber")
print(ls_resp)
#ls_resp[0].item[-2].title
for record in ls_resp[0].item:
    print(record.id, "\t", record.alias)

df_api.collectionView("projshare")
df_api.setContext("u/markmoujabber")
parent_collection = "markmoujabber"
parameters = "C:\Users\admin\Desktop\MEMT680\HW4\making_figures\src\making_figures\FantasyFootballWeekly.csv"
import json

json.dumps(parameters)

dc_resp = df_api.dataCreate(
    "my project data",
    metadata=json.dumps(parameters),
    parent_id=parent_collection,
    # The parent collection, whose alias is your username
)
dc_resp

record_id = dc_resp[0].data[0].id
print(record_id)

du_resp = df_api.dataUpdate(
    record_id,
    title="Fantasy Football Stats",
    metadata=json.dumps({"appended_metadata": True}),
)
print(du_resp)

dv_resp = df_api.dataView(record_id)
print(dv_resp)

metadata = json.loads(dv_resp[0].data[0].metadata)
print(metadata)

