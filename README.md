# Pepper Supporter

論文を読むためのサポートをChatGPTにさせる目的で作られたコードです.

# Development

## Git Prefix

| Prefix | Definition                  |
|--------|-----------------------------|
| add    | クラスや関数などを追加したときに使用する        |
| doc    | ドキュメントを書き換えたり作成したりしたときに使用する |

## Git Branching Strategy

| Branch  | Description                      | Parent  | Marge Into |
|---------|----------------------------------|---------|------------|
| main    | 安定版のコードが設置されるブランチ                | Nothing | Nothing    |
| develop | README.mdの書き換え, featブランチの大本のブランチ | main    | main       |
| feat/*  | featブランチ. コードはこのブランチで書き換えられる.    | develop | develop    |

*README.md* は *develop* ブランチから *main* ブランチにマージしたいときに変更する.

# Update History

## 0.0.2

- READMEにGitブランチ戦略について記述しました
- BaseFileAssistantを実装しました
- BaseFileAssistantのexampleを実装しました


## 0.0.1

- 基本となるBaseAssistantクラスを実装しました
- BaseAssistantクラスをテストするためのexampleを書きました
- READMEを作成しました