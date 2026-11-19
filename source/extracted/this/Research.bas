Attribute VB_Name = "Research"
Option Explicit

Private Function Guess(ByVal doc As SldWorks.ModelDoc2) As String
    On Error Resume Next
    Dim obj As Object, seg As SldWorks.SketchSegment, sk As SldWorks.Sketch, ft As SldWorks.Feature
    Set obj = doc.SelectionManager.GetSelectedObject6(1, -1)
    If TypeOf obj Is SldWorks.SketchSegment Then
        Set seg = obj
        Set sk = seg.GetSketch
        Guess = "sketch"
        If seg.GetType = swSketchSPLINE Then Guess = "spline"
        If sk.Is3D Then Guess = "3D " & Guess
    ElseIf TypeOf obj Is SldWorks.Feature Then
        Set ft = obj
        Guess = ft.GetTypeName2
        If Guess = "3DProfileFeature" Then Guess = "3D sketch"
        If Guess = "ProfileFeature" Then Guess = "sketch"
    End If
End Function

Public Sub main()
    On Error GoTo failed
    Dim app As SldWorks.SldWorks, doc As SldWorks.ModelDoc2, fs As Object
    Dim helper As String, folder As String, topic As String, f As Object, job As String
    Set app = Application.SldWorks
    Set doc = app.ActiveDoc
    If doc Is Nothing Then Exit Sub
    Set fs = CreateObject("Scripting.FileSystemObject")
    folder = fs.GetParentFolderName(app.GetCurrentMacroPathName)
    helper = fs.BuildPath(folder, "research.py")
    If Not fs.FileExists(helper) Then Err.Raise 5, , "Place research.py beside the saved .swp."
    topic = Trim$(InputBox("Public search terms only. Optional: add a symptom. No model is uploaded.", "Research this", Guess(doc)))
    If Len(topic) = 0 Then Exit Sub
    job = fs.BuildPath(fs.GetSpecialFolder(2), fs.GetTempName)
    Set f = fs.CreateTextFile(job, True, True)
    f.Write topic
    f.Close
    CreateObject("WScript.Shell").Run "py -3 """ & helper & """ --job """ & job & """", 1, False
    Exit Sub
failed:
    MsgBox Err.Description & vbCrLf & "Requires the Windows Python 3 launcher (py -3)."
End Sub
