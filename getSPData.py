

"""
WORK IN PROGRESS

var siteUrl = "https://qa-share.ahsnet.ca/teams/kmqa",
listId          = "{C9B991B4-2BC7-4169-8E8B-9270C604890B}";
busNeedListID   = "{9DC112D0-A174-4C6E-93A2-C46287E0530E}";
delivListID     = "{71557B2C-B9DD-4EA6-B355-882D363C0D13}";
solutListID     = "{70A9B3E2-E842-44D2-BF10-55A091045E95}";


$.get(siteUrl + "/_vti_bin/owssvr.dll?Cmd=Display&XMLDATA=TRUE&List=" + listId, function( xml ) {
    var data = new google.visualization.DataTable();
data.addColumn('string', 'Title'); //data.addColumn('string', 'Assigned');
data.addColumn('number', 'Sales in Millions');

var
zrow = xml.getElementsByTagName("z:row");
for (var
i = 0;
i < zrow.length;
i + +) {
    data.addRow([zrow[i].getAttribute("ows_Title"), parseInt(zrow[i].getAttribute("ows_g6ur"))]);
}
"""