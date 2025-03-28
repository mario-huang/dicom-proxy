# dicom-proxy

DICOM DIMSE 代理服务

## 支持的DIMSE服务

-   C-Echo
-   C-Find
-   C-Move

## 功能特性

-   简单易用
-   支持Docker部署
-   多客户端配置
-   调试日志开关

## 应用场景

当您只有一个AE（例如来自医院PACS）但需要多个应用访问时，本代理工具可以：
- 作为中间代理接收多个客户端的请求
- 统一转发到上游PACS系统
- 管理不同客户端的AE Title和网络配置

## 运行方式

### 方式一：源码运行
1. 克隆仓库并进入目录：
```bash
git clone git@github.com:mario-huang/dicom-proxy.git
cd dicom-proxy
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 启动服务：
```bash
python src/main.py
```

### 方式二：Docker部署
```bash
docker compose up -d
```

## 配置说明

编辑`config.json`文件：

```json
{
    // 启用调试日志
    "debug": true,
    
    // 代理服务器配置
    "proxy": {
        "aet": "DicomProxy",     // 代理AE Title
        "address": "0.0.0.0",    // 监听地址
        "port": 11112            // 监听端口
    },
    
    // 上游PACS配置 
    "server": {
        "aet": "UpstreamPacs",   // PACS的AE Title
        "address": "192.168.1.1",// PACS IP地址
        "port": 4242             // PACS端口
    },
    
    // 客户端配置列表
    "clients": [
        {
            "aet": "ClientAET",  // 客户端AE Title
            "address": "192.168.1.2", // 客户端IP
            "port": 6000         // 客户端端口
        }
    ]
}
```

## 注意事项
1. 请确保防火墙开放代理端口（默认11112）
2. 客户端配置需要与各应用端的DICOM设置保持一致
3. 生产环境建议关闭debug模式
