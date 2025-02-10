# Pepper Supporter

論文を読むためのサポートをChatGPTにさせる目的で作られたコードです.

# Development

## Git Prefix

| Prefix  | Definition                  |
|---------|-----------------------------|
| add     | クラスや関数などを追加したときに使用する        |
| doc     | ドキュメントを書き換えたり作成したりしたときに使用する |
| mov     | ファイルの移動や消去を行ったときに使う         |
| replace | クラスや関数などを消去したときに使用する        |

基本的に破壊的な変更は認められない. 破壊的な変更を行う場合は *add* プレフィックスで新しいインターフェイスの関数等を追加し,
十分に新しい関数が使われるようになったら *replace* プレフィックスで古い関数と置き換える.

新しい関数を追加したときは古い関数に *deprecated* であることがわかるようにマークをつける.

古い関数を置き換えるときは次のようにする.

```python
def functionA():
    return functionA_v2()


def functionA_v2():
    # NEW IMPLEMENTATION
    return


def functionB():
    return functionB_v5()


# REMOVE THIS
# def functionB_v4():
#    # OLD FUNCTION
#    return


def functionB_v5():
    # NEW IMPREMENTATION
    return
```

## Git Branching Strategy

| Branch  | Description                      | Parent  | Marge Into |
|---------|----------------------------------|---------|------------|
| main    | 安定版のコードが設置されるブランチ                | Nothing | Nothing    |
| develop | README.mdの書き換え, featブランチの大本のブランチ | main    | main       |
| feat/*  | featブランチ. コードはこのブランチで書き換えられる     | develop | develop    |

*README.md* は *develop* ブランチから *main* ブランチにマージしたいときに変更する.

# Update History

## 0.0.4

- 基本的な機能を実装しました

## 0.0.3

- Git Prefixを追加しました
- GUI用のExampleとAssistantのExampleを分離するために, AssistantのExampleを移動させました

## 0.0.2

- READMEにGitブランチ戦略について記述しました
- BaseFileAssistantを実装しました
- BaseFileAssistantのexampleを実装しました

## 0.0.1

- 基本となるBaseAssistantクラスを実装しました
- BaseAssistantクラスをテストするためのexampleを書きました
- READMEを作成しました