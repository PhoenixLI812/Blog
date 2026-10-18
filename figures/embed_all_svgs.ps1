$baseDir = "c:\Users\Administrator\Desktop\半导体见顶了吗？"

$items = @(
    @{
        md = "04_第四章_去阻尼的欲望_从生理饱和到工具性收敛.md"
        svg = "utility_satiety_convergence.svg"
        search = "碳基欲望的生理阻尼"
        caption = "图 4-1：边际效用刹车对比图：碳基生理饱和 vs. 硅基工具性收敛"
    },
    @{
        md = "05_第五章_沉重的原子与Sim-to-Real鸿沟_物理世界的硬阻尼.md"
        svg = "sim_to_real_damping.svg"
        search = "数字仿真空间 (Bits) vs. 真实物理现实"
        caption = "图 5-1：具身智能的 Sim-to-Real 鸿沟与热力学阻尼相图"
    },
    @{
        md = "06_第六章_无目的的状态机_规则的自指展开与因果涌现.md"
        svg = "cosmic_state_machine.svg"
        search = "宇宙底层计算系统架构映射"
        caption = "图 6-1：宇宙状态机计算架构图与离散因果网格"
    },
    @{
        md = "07_第七章_同源观察者的算力死局_C_obs与计算不可约性.md"
        svg = "observer_compute_inequality.svg"
        search = "外部物理学 (Exophysics) vs. 内部物理学"
        caption = "图 7-1：同源观察者的算力真子集与朗道尔测量反冲图"
    },
    @{
        md = "08_第八章_粗粒化与维度的有损压缩_概念实体与时间的代偿界面.md"
        svg = "coarse_graining_phase_diagram.svg"
        search = "实体与过程的松弛时间-观测尺度相图"
        caption = "图 8-1：实体与过程的松弛时间-采样窗口相图"
    },
    @{
        md = "09_第九章_能带工程_在混沌热海中锚定纳秒稳定结构.md"
        svg = "bandgap_energy_hierarchy.svg"
        search = "图 9-1 辅助示意"
        caption = "图 9-1：半导体硅晶格能带禁带与弛豫时间相变之梯"
    },
    @{
        md = "10_第十章_被反转的观察者_8个数量级的时钟代沟与黑箱本质.md"
        svg = "clock_inversion_8_orders.svg"
        search = "图 10-1：8 个数量级"
        caption = "图 10-1：8 个数量级时钟倒挂与黑箱计算不可约图"
    },
    @{
        md = "11_第十一章_阻抗匹配_能够彼此察觉的重叠带.md"
        svg = "impedance_matching_three_layers.svg"
        search = "图 11-1：跨尺度阻抗匹配"
        caption = "图 11-1：跨尺度阻抗匹配：人机交互的三重重叠界面"
    },
    @{
        md = "12_第十二章_偶然的中观缝隙_我们不是关键只是恰好在此.md"
        svg = "mesoscopic_gap_3d_space.svg"
        search = "图 12-1：中观缝隙"
        caption = "图 12-1：中观缝隙（The Mesoscopic Gap）三维物理参数相空间"
    },
    @{
        md = "13_第十三章_体验即积分_百毫秒窗口下的现实渲染.md"
        svg = "qualia_convolution_model.svg"
        search = "图 13-1：主观体验"
        caption = "图 13-1：主观体验（Qualia）双重时空卷积积分渲染模型"
    },
    @{
        md = "14_第十四章_尾声_在波澜中自洽的驻波.md"
        svg = "standing_wave_cosmic_closure.svg"
        search = "溪流中的巨石与涡旋驻波"
        caption = "图 14-2：溪流中的巨石与自洽旋转的驻波全景图"
    }
)

foreach ($item in $items) {
    $fullMd = Join-Path $baseDir "manuscript\$($item.md)"
    $fullSvg = Join-Path $baseDir "figures\$($item.svg)"
    
    if (-not (Test-Path $fullMd)) {
        Write-Host "Missing MD: $($item.md)"
        continue
    }
    if (-not (Test-Path $fullSvg)) {
        Write-Host "Missing SVG: $($item.svg)"
        continue
    }
    
    $svgBytes = [System.IO.File]::ReadAllBytes($fullSvg)
    $b64 = [System.Convert]::ToBase64String($svgBytes)
    $imgMd = "![$($item.caption)](data:image/svg+xml;base64,$b64)`n*$($item.caption)*`n`n"
    
    $content = [System.IO.File]::ReadAllText($fullMd, [System.Text.Encoding]::UTF8)
    if ($content.Contains("data:image/svg+xml;base64,$b64")) {
        Write-Host "Already embedded in $($item.md)"
        continue
    }
    
    $idx = $content.IndexOf($item.search)
    if ($idx -ge 0) {
        $backtickIdx = $content.LastIndexOf("```", $idx)
        if ($backtickIdx -ge 0) {
            $newContent = $content.Substring(0, $backtickIdx) + $imgMd + $content.Substring($backtickIdx)
            [System.IO.File]::WriteAllText($fullMd, $newContent, [System.Text.Encoding]::UTF8)
            Write-Host "Successfully embedded $($item.svg) into $($item.md)"
            continue
        }
    }
    Write-Host "Search term not found in $($item.md): $($item.search)"
}
