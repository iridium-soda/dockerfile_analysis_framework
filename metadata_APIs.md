# APIs for metadatas

> 每个tag的~~image name, created date, update date~~, layers' history，layer size, ~~short description, full description~~

都不需要认证
- created date: No info provided
- tags:https://hub.docker.com/v2/namespaces/library/repositories/ubuntu/tags : `name`
- Updated date: https://hub.docker.com/v2/namespaces/library/repositories/ubuntu/tags :`results.images.last_pulled`
- layer size: https://hub.docker.com/v2/repositories/library/ubuntu/tags/18.04/images
- build history: https://hub.docker.com/v2/repositories/library/ubuntu/tags/18.04/images
- Overview: curl -X GET https://hub.docker.com/v2/repositories/library/nginx/
    - Full在`"full_description"`
    - Short在`description`

dockerhub的架构如下：
namespace-repo-tags-digest(os/architecture)

Update time应该以每个image为单位，

以json格式存储

重新写一个

### json example

For a single image repo in `results`:
```json
{
    "image_name":"",
    "created_at":"",
    "images":[
        {
            "tag":"",
            "digest":"",
            "last_pulled":"",
            "os":"linux",
            "architecture":"amd64",
            "layers":[
                {
                    "size":0,
                    "instruction":"ARG RELEASE"
                },
                {
                    "size":0,
                    "instruction":"ARG LAUNCHPAD_BUILD_ARCH"
                },
                {
                    "size":0,
                    "instruction":"LABEL org.opencontainers.image.ref.name=ubuntu"
                },
                {
                    "size":0,
                    "instruction":"LABEL org.opencontainers.image.version=18.04"
                },
                {
                    "digest":"sha256:7c457f213c7634afb95a0fb2410a74b7b5bc0ba527033362c240c7a11bef4331",
                    "size":25691281,
                    "instruction":"ADD file:3c74e7e08cbf9a87694ce6fa541af617599680fa54d9e48556fc0fbc120b4a83 in /"
                },
                {
                    "size":0,
                    "instruction":"CMD [\"/bin/bash\"]"
                }
            ]
        }
    ]
}
```