spawn tui
expect {
  "│ Summary │ Passes │ Failures │ Skipped │ Xfails │ Xpasses │ Warnings │ Errors │ Full Output │ Quit (Q) │"
  {
    send "q"
    sleep 5
    exit
  }
}
