Add-Type -AssemblyName System.Windows.Forms

# 创建一个窗体对象
$form = New-Object System.Windows.Forms.Form
$form.Text = "Media Batch Converter (Language Selector)"
$form.Width = 523
$form.Height = 240
$form.FormBorderStyle = "FixedSingle"
$form.StartPosition = "CenterScreen"

# 创建 TableLayoutPanel
$tableLayoutPanel = New-Object System.Windows.Forms.TableLayoutPanel
$tableLayoutPanel.Dock = [System.Windows.Forms.DockStyle]::Fill
$tableLayoutPanel.ColumnCount = 1
$tableLayoutPanel.RowCount = 3
$tableLayoutPanel.ColumnStyles.Add((New-Object System.Windows.Forms.ColumnStyle([System.Windows.Forms.SizeType]::Percent, 100)))
$tableLayoutPanel.RowStyles.Add((New-Object System.Windows.Forms.RowStyle([System.Windows.Forms.SizeType]::Percent, 50)))
$tableLayoutPanel.RowStyles.Add((New-Object System.Windows.Forms.RowStyle([System.Windows.Forms.SizeType]::Absolute, 50)))
$tableLayoutPanel.RowStyles.Add((New-Object System.Windows.Forms.RowStyle([System.Windows.Forms.SizeType]::Percent, 50)))
$form.Controls.Add($tableLayoutPanel)

# 创建一个下拉列表框
$comboBox = New-Object System.Windows.Forms.ComboBox
$comboBox.Anchor = [System.Windows.Forms.AnchorStyles]::None
$comboBox.Size = New-Object System.Drawing.Size(200,30)
$comboBox.Items.AddRange(@("🇺🇸 English(US)", "🇨🇳 中文(中华人民共和国)", "🇹🇼 中文(中华民国台湾)"))
$tableLayoutPanel.Controls.Add($comboBox, 0, 0)

# 创建一个按钮
$button = New-Object System.Windows.Forms.Button
$button.Anchor = [System.Windows.Forms.AnchorStyles]::None
$button.Size = New-Object System.Drawing.Size(100, 30)
$button.Text = "OK"
$button.Add_Click({
    $selectedLanguage = $comboBox.SelectedItem
    switch ($selectedLanguage) {
        "English(US)" {
            Start-Process "python" "en-us.py"
        }
        "中文(中华人民共和国)" {
            Start-Process "python" "zh-cn.py"
        }
        "中文(台湾繁体)" {
            Start-Process "python" "zh-tw.py"
        }
    }
    $form.Close()
})
$tableLayoutPanel.Controls.Add($button, 0, 2)

# 显示窗体
$form.ShowDialog() | Out-Null
