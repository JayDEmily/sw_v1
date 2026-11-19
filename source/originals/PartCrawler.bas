Attribute VB_Name = "PartCrawler"
Option Explicit

Private report As String
Private stage As String
Private ui As Object

Private Sub note(ByVal msg As String)
    Dim n As Integer
    n = FreeFile
    Open report For Append As #n
    Print #n, Format$(Now, "hh:nn:ss") & "  " & msg
    Close #n
    Debug.Print msg
End Sub

Private Sub progress(ByVal msg As String)
    stage = msg
    On Error Resume Next
    ui.SetStatusBarText msg
    DoEvents
    On Error GoTo 0
End Sub

Private Function probe(ByVal fc As SldWorks.Face2, ByVal mm As Double, ByVal reverse As Boolean) As String
    On Error GoTo bad
    Dim sh As SldWorks.Body2, shifted As SldWorks.Body2
    Set sh = fc.CreateSheetBody
    If sh Is Nothing Then
        probe = "NOT TESTED: sheet creation failed"
        Exit Function
    End If
    Set shifted = sh.MakeOffset(mm / 1000#, reverse)
    If shifted Is Nothing Then
        probe = "NO OFFSET BODY"
    Else
        probe = "body returned"
    End If
    Exit Function
bad:
    probe = "API ERROR " & Err.Number & ": " & Err.Description
End Function

Public Sub main()
    Dim app As SldWorks.SldWorks, doc As SldWorks.ModelDoc2, part As SldWorks.PartDoc
    Dim ft As SldWorks.Feature, b As SldWorks.Body2, fc As SldWorks.Face2
    Dim fault As SldWorks.FaultEntity, owner As SldWorks.Feature
    Dim bodies As Variant, v As Variant, box As Variant
    Dim w As Boolean, e As Long, i As Long, idx As Long, typ As Long
    Dim answer As String, mm As Double, who As String, a As String, z As String
    Dim nb As Long, issues As Long, tested As Long, flagged As Long, badBodies As Long
    Dim bodyOK As Boolean, msg As String
    On Error GoTo failed
    Set app = Application.SldWorks
    Set doc = app.ActiveDoc
    If doc Is Nothing Then Exit Sub
    If doc.GetType <> 1 Then
        MsgBox "Open a part, not an assembly or drawing."
        Exit Sub
    End If
    Set part = doc
    Set ui = app.Frame
    answer = InputBox("Optional per-face offset test in mm (both directions). Enter 0 for baseline checks only. Cancel to quit.", "Part crawler", "10")
    If Len(answer) = 0 Then Exit Sub
    If Not IsNumeric(answer) Then Exit Sub
    mm = CDbl(answer)
    If mm < 0 Then Exit Sub
    report = Environ$("TEMP") & "\SW_PartCrawler_" & Format$(Now, "yyyymmdd_hhnnss") & ".txt"
    note "START " & doc.GetTitle & " | " & doc.ConfigurationManager.ActiveConfiguration.Name & " | SW revision " & app.RevisionNumber
    note "Top-level feature scan, current state (no rebuild)."
    Set ft = doc.FirstFeature
    Do While Not ft Is Nothing
        progress "Checking feature " & ft.Name
        e = ft.GetErrorCode2(w)
        If e <> 0 Then
            note ft.Name & " [" & ft.GetTypeName2 & "] " & IIf(w, "warning ", "error ") & e
            issues = issues + 1
        End If
        Set ft = ft.GetNextFeature
    Loop
    For typ = 0 To 1 ' solid, sheet; include hidden bodies
        bodies = part.GetBodies2(typ, False)
        If IsArray(bodies) Then
            For Each v In bodies
                Set b = v
                nb = nb + 1
                progress "Checking body " & b.Name
                Set fault = b.Check3
                bodyOK = True
                If Not fault Is Nothing Then
                    For i = 0 To fault.Count - 1
                        note "Body " & b.Name & " fault " & fault.ErrorCode(i)
                        bodyOK = False
                    Next i
                End If
                If bodyOK Then
                    note "Body " & b.Name & ": no Check3 faults reported."
                Else
                    badBodies = badBodies + 1
                    note "Offset tests skipped on faulty body: " & b.Name
                End If
                If mm > 0 And bodyOK Then
                    idx = 0
                    Set fc = b.GetFirstFace
                    Do While Not fc Is Nothing
                        idx = idx + 1
                        who = b.Name & " face " & idx
                        Set owner = fc.GetFeature
                        If Not owner Is Nothing Then who = who & " [" & owner.Name & "]"
                        progress "Offset test: " & who
                        a = probe(fc, mm, False)
                        z = probe(fc, mm, True)
                        tested = tested + 1
                        note who & ", " & mm & " mm: along sheet normal=" & a & "; opposite=" & z
                        If a <> "body returned" Or z <> "body returned" Then
                            flagged = flagged + 1
                            box = fc.GetBox
                            If IsArray(box) Then note "  Approximate bounding box centre XYZ (mm): " & _
                                Round(500# * (box(0) + box(3)), 2) & ", " & _
                                Round(500# * (box(1) + box(4)), 2) & ", " & _
                                Round(500# * (box(2) + box(5)), 2)
                        End If
                        Set fc = fc.GetNextFace
                    Loop
                End If
            Next v
        End If
    Next typ
    msg = "Feature warnings/errors: " & issues & "; bodies checked: " & nb & "; bodies reporting faults: " & badBodies & "." & vbCrLf & _
          "Faces probed: " & tested & "; faces with incomplete or unsuccessful offsets: " & flagged & "."
    note "COMPLETE. " & msg
    progress "Part crawler finished"
    MsgBox msg & vbCrLf & report, vbInformation, "Part crawler"
    Exit Sub
failed:
    msg = "INCOMPLETE at " & stage & ": " & Err.Number & " " & Err.Description
    On Error Resume Next
    If Len(report) <> 0 Then note msg
    MsgBox msg & vbCrLf & report, vbExclamation, "Part crawler"
End Sub
