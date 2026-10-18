[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$baseDir = "c:\Users\Administrator\Desktop\半导体见顶了吗？"

$map = @(
    @{ prefix = "04_"; svg = "utility_satiety_convergence.svg"; marker = "04"; cap = "图 4-1：边际效用刹车对比图：碳基生理饱和 vs. 硅基工具性收敛" },
    @{ prefix = "05_"; svg = "sim_to_real_damping.svg"; marker = "05"; cap = "图 5-1：具身智能的 Sim-to-Real 鸿沟与热力学阻尼相图" },
    @{ prefix = "06_"; svg = "cosmic_state_machine.svg"; marker = "06"; cap = "图 6-1：宇宙状态机计算架构图与离散因果网格" },
    @{ prefix = "07_"; svg = "observer_compute_inequality.svg"; marker = "07"; cap = "图 7-1：同源观察者的算力真子集与朗道尔测量反冲图" },
    @{ prefix = "08_"; svg = "coarse_graining_phase_diagram.svg"; marker = "08"; cap = "图 8-1：实体与过程的松弛时间-采样窗口相图" },
    @{ prefix = "09_"; svg = "bandgap_energy_hierarchy.svg"; marker = "09"; cap = "图 9-1：半导体硅晶格能带禁带与弛豫时间相变之梯" },
    @{ prefix = "10_"; svg = "clock_inversion_8_orders.svg"; marker = "10"; cap = "图 10-1：8 个数量级时钟倒挂与黑箱计算不可约图" },
    @{ prefix = "11_"; svg = "impedance_matching_three_layers.svg"; marker = "11"; cap = "图 11-1：跨尺度阻抗匹配：人机交互的三重重叠界面" },
    @{ prefix = "12_"; svg = "mesoscopic_gap_3d_space.svg"; marker = "12"; cap = "图 12-1：中观缝隙（The Mesoscopic Gap）三维物理参数相空间" },
    @{ prefix = "13_"; svg = "qualia_convolution_model.svg"; marker = "13"; cap = "图 13-1：主观体验（Qualia）双重时空卷积积分渲染模型" },
    @{ prefix = "14_"; svg = "standing_wave_cosmic_closure.svg"; marker = "14"; cap = "图 14-2：溪流中的巨石与自洽旋转的驻波全景图" }
)

foreach ($item in $map) {
    $md = Get-ChildItem -Path "$baseDir\manuscript\$($item.prefix)*.md" | Select-Object -First 1
    $svgPath = "$baseDir\figures\$($item.svg)"
    if ($md -and (Test-Path $svgPath)) {
        $svgBytes = [System.IO.File]::ReadAllBytes($svgPath)
        $b64 = [System.Convert]::ToBase64String($svgBytes)
        $img = "`n![$($item.cap)](data:image/svg+xml;base64,$b64)`n*$($item.cap)*`n`n"
        
        $text = [System.IO.File]::ReadAllText($md.FullName, [System.Text.Encoding]::UTF8)
        if (-not $text.Contains("data:image/svg+xml;base64,$b64")) {
            # Find the first code fence ``` in section 1 or 2
            $pos = $text.IndexOf("```")
            if ($pos -ge 0) {
                $newText = $text.Substring(0, $pos) + $img + $text.Substring($pos)
                [System.IO.File]::WriteAllText($md.FullName, $newText, [System.Text.Encoding]::UTF8)
                Write-Host "Success for $($md.Name)"
            }
        } else {
            Write-Host "Already exists in $($md.Name)"
        }
    }
}