# timetable_extractor

## 開発目的
このアプリケーションは、忘れ物を減らすために通知機能を活用し、ユーザーの意識向上を目的としています。
LINEの通知機能を利用して、必要な持ち物や準備物の情報を効果的に伝達します。

## 技術スタック
- **データベース**: MongoDB (Docker上で動作)
    - NOSQLデータベースを採用し、時間割データの柔軟な管理を実現
    - コンテナ化によりデータの移行性を向上

- **バックエンド**:
    - OCR処理: Python
        - 豊富なOCRライブラリを活用
        - 将来的にNode.jsやGoへの移行も検討中

## 成果と今後の展望
- 実験段階での運用により、以下の成果を確認
    - 視認性の向上
    - 管理性の改善

### 今後の課題
1. ユーザーニーズの調査
2. 利用者からのフィードバック収集
3. 管理機能の使いやすさ向上
4. システムの汎用性向上

