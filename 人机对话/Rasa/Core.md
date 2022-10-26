# Core

## 1. 简介

## 2. Stories

```
Rasa故事是一种训练数据形式，用于训练Rasa的对话管理模型。
故事是用户和 AI 助手之间对话的表示形式，转换为特定格式，其中用户输入表示为相应的意图（+实体），而助手的响应表示为相应的操作名称。
```

### 2.1 格式

```markdown
## greet + location/price + cuisine + num people    <!-- name of the story - just for debugging -->
* greet
   - action_ask_howcanhelp
* inform{"location": "rome", "price": "cheap"}  <!-- user utterance, in format intent{entities} -->
   - action_on_it
   - action_ask_cuisine
* inform{"cuisine": "spanish"}
   - action_ask_numpeople        <!-- action that the bot should execute -->
* inform{"people": "six"}
   - action_ack_dosearch
```

**stories的构成：**

```
1. 一个故事以一个名字开始，前面有两个哈希## story_03248462。你可以随心所欲地称呼这个故事，但是给它们起到描述性的名称对于调试来说非常有用！

2. 故事的结尾用换行符表示，然后新故事再次以##开始。

3. 用户发送的消息显示为以*开头的行，格式为intent{"entity1": "value", "entity2": "value"}

4. 机器人执行的操作显示为以-开头的行，并包含操作的名称。

5. 操作返回的事件紧跟在该操作之后的行上。例如，如果某个操作返回一个事件，则此事件显示为 SlotSetslot{"slot_name": "value"}
```

**用户消息 (User Messages)**

```
在编写故事时，不必处理用户发送的消息的特定内容。相反，您可以利用 NLU 管道的输出，这允许您仅使用意向和实体的组合来引用用户可以发送的所有可能的消息来表示相同的内容。

在此处包含实体也很重要，因为策略会学习根据意向和实体的组合来预测下一个操作（但是，您可以使用 use_entities 属性更改此行为）。
```

**Actions**

```
在编写故事时，您将遇到两种类型的操作：话语(utterances)和自定义操作(custom actions)。话语是机器人可以使用的硬编码消息。另一方面，自定义操作涉及正在执行的自定义代码。

机器人执行的所有操作（包括话语和自定义操作）都显示为以-开头的行，后跟操作的名称。

所有话语(utterances)必须以utter_前缀开头，并且必须与域中定义的模板的名称匹配。

对于自定义操作(custom actions)，操作名称是您选择从自定义操作类的name方法返回的字符串。尽管对命名自定义操作没有限制（与话语不同），但此处的最佳做法是在名称前面加上action_前缀。
```

**Events**

```
诸如设置插槽或激活/停用表单之类的事件必须作为故事的一部分明确地写出来。当自定义操作已经是故事的一部分时，必须单独包含自定义操作返回的事件可能看起来是多余的。但是，由于 Rasa 在训练期间无法确定这一事实，因此此步骤是必要的。
```

**槽事件(Slot Events)**

```
插槽事件写为 - slot{"slot_name": "value"}。如果此槽是在自定义操作内设置的，则会将其写在紧跟在自定义操作事件之后的行上。如果自定义操作将槽值重置为 None，则相应的事件将为-slot{"slot_name": null}
```

**表单事件(Form Events)**

```
在处理故事中的形式时，需要记住三种事件。

1. 表单操作事件（例如 - restaurant_form）在开始时首次启动表单时使用，并且在表单已处于活动状态时恢复表单操作时使用。

2. 表单激活事件（例如 form{"name": "restaurant_form"}）紧接在第一个表单操作事件之后使用。- 

3. 表单停用事件（例如 - form{"name": null}），用于停用表单。
```

### 2.2 Checkpoints and OR statements

**Checkpoints**

```
您可以使用 > checkpoints 来模块化和简化训练数据。检查点可能很有用，但不要过度使用它们,使用大量检查点会很快使示例故事难以理解。如果故事块在不同的故事中经常重复，则使用它们是有意义的，但是没有检查点的故事更容易阅读和编写。下面是一个包含检查点的示例故事文件（请注意，您可以一次附加多个检查点）：
```

```markdown
## first story
* greet
   - action_ask_user_question
> check_asked_question

## user affirms question
> check_asked_question
* affirm
  - action_handle_affirmation
> check_handled_affirmation

## user denies question
> check_asked_question
* deny
  - action_handle_denial
> check_handled_denial

## user leaves
> check_handled_denial
> check_handled_affirmation
* goodbye
  - utter_goodbyema
```

```
与常规故事不同，检查点不限于从用户的输入开始。只要将检查点插入到主要故事的正确位置，第一个事件也可以是操作或话语。
```

**OR语句**

```
另一种写短故事或以相同方式处理多个意图的方法是使用OR语句。例如，如果您要求用户确认某些内容，并且您希望以相同的方式处理affirm和thankyou意图。下面的故事将在训练时转换为两个故事：
```

```markdown
## story
...
  - utter_ask_confirm
* affirm OR thankyou
  - action_handle_affirmation
```

```
过度使用这些功能（检查点和 OR 语句）会减慢训练速度。
```

### 2.3 端到端的故事评估格式

```
端到端故事格式是一种将 NLU 和 Core 训练数据合并到单个文件中以进行评估的格式。您可以在此处阅读更多相关信息。

此格式仅用于端到端评估，不能用于训练。
```

## 3. Domain

```
域文件包含有：intents entities slots actions，还包含templates（可选）
```

### 3.1 例子

```yaml
intents:
  - greet
  - goodbye
  - affirm
  - deny
  - mood_great
  - mood_unhappy
  - bot_challenge

actions:
- utter_greet
- utter_cheer_up
- utter_did_that_help
- utter_happy
- utter_goodbye
- utter_iamabot

templates:
  utter_greet:
  - text: "Hey! How are you?"

  utter_cheer_up:
  - text: "Here is something to cheer you up:"
    image: "https://i.imgur.com/nGF1K8f.jpg"

  utter_did_that_help:
  - text: "Did that help you?"

  utter_happy:
  - text: "Great, carry on!"

  utter_goodbye:
  - text: "Bye"

  utter_iamabot:
  - text: "I am a bot, powered by Rasa."
```

```
1. NLU模型中将定义需要包含在域中的intents与entities

2. 槽(Slots)保存了我们希望在对话期间跟踪的信息
例如，分类槽(categorical slot)将定义为:
slots:
   risk_level:
      type: categorical
      values:
      - low
      - medium
      - high

3. actions是机器人实际可以执行的操作，例如：响应用户；进行外部 API 调用，查询数据库，或其他几乎任何东西！
```

### 3.2 自定义操作和槽

```
要引用域中的槽，需要按其模块路径引用它们。若要引用自定义操作，请使用其名称。例如，如果您有一个名为my_actions的模块，其中包含一个类MyAwesomeAction，而模块my_slots包含MyAwesomeSlot，则可以将以下行添加到域文件中：

actions:
  - my_custom_action
  ...

slots:
  - my_slots.MyAwesomeSlot
  


在上边例子中，MyAwesomeAction的name函数需要返回my_custom_action
```

### 3.3 话语模板(utterance templates)

```
话语模板是机器人将发回给用户的消息。有两种方法可以使用这些模板：

1. 如果模板的名称以utter_开头，则该话语可以直接用作操作。将以下话语模板添加到域中：
templates:
  utter_greet:
  - text: "Hey! How are you?"
  
之后，您可以将模板用作故事中的操作：
## greet the user
* intent_greet
  - utter_greet
  
当utter_greet作为操作运行时，它会将消息从模板发送回用户。

2. 您可以使用模板通过调度程序dispatcher.utter_message(template="utter_greet")从自定义操作生成响应消息，这允许您将生成消息的逻辑与实际副本分开。在自定义操作代码中，可以基于模板发送消息，如下所示：
```

```python
from rasa_sdk.actions import Action

class ActionGreet(Action):
  def name(self):
      return 'action_greet'

  def run(self, dispatcher, tracker, domain):
      dispatcher.utter_message(template="utter_greet")
      return []
```

### 3.4 图像和按钮

```
在域的 yaml 文件中定义的模板也可以包含图像和按钮：
注：如何显示定义的按钮取决于输出通道的实现。例如，命令行无法显示按钮或图像，但会尝试通过打印选项来模拟它们。
```

```yaml
templates:
  utter_greet:
  - text: "Hey! How are you?"
    buttons:
    - title: "great"
      payload: "great"
    - title: "super sad"
      payload: "super sad"
  utter_cheer_up:
  - text: "Here is something to cheer you up:"
    image: "https://i.imgur.com/nGF1K8f.jpg"
```

### 3.5 自定义输出负载(output payloads)

```
可以使用custom:键将任意输出发送到输出通道。请注意，由于域采用 yaml 格式，因此应首先将 json 有效负载转换为 yaml 格式。

例如，尽管日期选取器不是话语模板中的已定义参数，因为它们不受大多数通道支持，但 Slack 日期选取器可以按如下方式发送：
```

```yaml
templates:
  utter_take_bet:
  - custom:
      blocks:
      - type: section
        text:
          text: "Make a bet on when the world will end:"
          type: mrkdwn
        accessory:
          type: datepicker
          initial_date: '2019-05-21'
          placeholder:
            type: plain_text
            text: Select a date
```

### 3.6 特定于通道的话语

```
如果您有某些只想发送到特定通道的话语，则可以使用channel:键指定此项。该值应与通道的OutputChannel类的name()方法中定义的名称匹配。如果创建仅在特定通道中起作用的自定义输出负载，则特定于通道的话语特别有用。
```

```yaml
templates:
  utter_ask_game:
  - text: "Which game would you like to play?"
    channel: "slack"
    custom:
      - # payload for Slack dropdown menu to choose a game
  - text: "Which game would you like to play?"
    buttons:
    - title: "Chess"
      payload: '/inform{"game": "chess"}'
    - title: "Checkers"
      payload: '/inform{"game": "checkers"}'
    - title: "Fortnite"
      payload: '/inform{"game": "fortnite"}'
```

```
每次机器人查找话语时，它都会首先检查是否存在任何特定于通道的已连接通道的模板。如果有，它将仅从这些话语中进行选择。如果未找到特定于通道的模板，它将从未定义channel的任何话语中进行选择。因此，最好始终为每个未指定的话语提供至少一个模板，以便机器人可以在所有环境（包括 shell 和交互式学习）中做出响应。
```

### 3.7 变量(variables)

```
还可以在模板中使用变量来插入在对话期间收集的信息。您可以在自定义python代码中执行此操作，也可以使用自动插槽填充机制。例如，如果您有一个如下模板：
```

```yaml
templates:
  utter_greet:
  - text: "Hey, {name}. How are you?"
```

```
Rasa 将自动用在名为 的插槽中找到的值填充该变量。name

在自定义代码中，可以使用以下命令检索模板：
```

```python
class ActionCustom(Action):
   def name(self):
      return "action_custom"

   def run(self, dispatcher, tracker, domain):
      # send utter default template to user
      dispatcher.utter_message(template="utter_default")
      # ... other code
      return []
```

```
如果模板包含用{my_variable}表示的变量，则可以通过将字段作为关键字参数传递给utter_message来为字段提供值：

dispatcher.utter_message(template="utter_greet", my_variable="my text")
```

### 3.8变化

```
如果你想随机改变发送给用户的响应，你可以列出多个响应，Rasa会随机选择其中一个，例如：
```

```yaml
templates:
  utter_greeting:
  - text: "Hey, {name}. How are you?"
  - text: "Hey, {name}. How is your day going?"
```

### 3.9 忽略某些意图的实体

```
如果您希望为某些意向忽略所有实体，则可以将use_entities: []参数添加到域文件中的意向中，如下所示：
```

```yaml
intents:
  - greet:
      use_entities: []
```

```
若要忽略某些实体或显式仅考虑某些实体，可以使用以下语法：
(这意味着这些意图的排除实体将不具体化，因此不会影响下一个操作预测。当您的意图不关心正在选取的实体时，这很有用。如果在没有此参数的情况下将意向列为正常，则实体将正常化。)
```

```yaml
intents:
- greet:
    use_entities:
      - name
      - first_name
    ignore_entities:
      - location
      - age
```

## 4. Response

```
如果您希望助手响应用户消息，则需要管理这些响应。在机器人的训练数据（故事）中，指定机器人应执行的操作。这些操作可以使用话语将消息发送回用户。

有三种方法可以管理这些话语：
1. 话语通常存储在您的域文件中
2. 检索操作响应是训练数据的一部分
3. 创建自定义 NLG 服务来生成响应
```

### 4.1 在域中包含话语(utterance)

```yaml
# all hashtags are comments :)
intents:
 - greet
 - default
 - goodbye
 - affirm
 - thank_you
 - change_bank_details
 - simple
 - hello
 - why
 - next_intent

entities:
 - name

slots:
  name:
    type: text

templates:
  utter_greet:
    - text: "hey there {name}!"  # {name} will be filled by slot (same name) or by custom action
  utter_channel:
    - text: "this is a default channel"
    - text: "you're talking to me on slack!"  # if you define channel-specific utterances, the bot will pick
      channel: "slack"                        # from those when talking on that specific channel
  utter_goodbye:
    - text: "goodbye 😢"   # multiple templates - bot will randomly pick one of them
    - text: "bye bye 😢"
  utter_default:   # utterance sent by action_default_fallback
    - text: "sorry, I didn't get that, can you rephrase it?"

actions:
  - utter_default
  - utter_greet
  - utter_goodbye
```

### 4.3 为机器人响应创建NLG服务

```
为了更改文本副本而重新训练机器人对于某些工作流来说可能并不理想。这就是为什么Core还允许您外包响应生成并将其与对话学习分开的原因。

助手仍将学习根据过去的对话预测操作并对用户输入做出反应，但它发回给用户的响应是在Rasa Core之外生成的。
```

如果助手想要向用户发送消息，它将调用外部 HTTP 服务器并发出POST请求。若要配置此终结点，需要创建一个endpoints.yml并将其传递给 run 或 server 脚本。endpoints.yml的内容应该是:

```yaml
nlg:
  url: http://localhost:5055/nlg    # url of the nlg endpoint
  # you can also specify additional parameters, if you need them:
  # headers:
  #   my-custom-header: value
  # token: "my_authentication_token"    # will be passed as a get parameter
  # basic_auth:
  #   username: user
  #   password: pass
# example of redis external tracker store config
tracker_store:
  type: redis
  url: localhost
  port: 6379
  db: 0
  password: password
  record_exp: 30000
# example of mongoDB external tracker store config
#tracker_store:
  #type: mongod
  #url: mongodb://localhost:27017
  #db: rasa
  #user: username
  #password: password
```

然后在启动服务器时将标志传递给命令：`enable-api``rasa run`

```
$ rasa run \
   --enable-api \
   -m examples/babi/models \
   --log-file out.log \
   --endpoints endpoints.yml
```

发送到终结点的请求的正文将如下所示：`POST`

```json
{
  "tracker": {
    "latest_message": {
      "text": "/greet",
      "intent_ranking": [
        {
          "confidence": 1.0,
          "name": "greet"
        }
      ],
      "intent": {
        "confidence": 1.0,
        "name": "greet"
      },
      "entities": []
    },
    "sender_id": "22ae96a6-85cd-11e8-b1c3-f40f241f6547",
    "paused": false,
    "latest_event_time": 1531397673.293572,
    "slots": {
      "name": null
    },
    "events": [
      {
        "timestamp": 1531397673.291998,
        "event": "action",
        "name": "action_listen"
      },
      {
        "timestamp": 1531397673.293572,
        "parse_data": {
          "text": "/greet",
          "intent_ranking": [
            {
              "confidence": 1.0,
              "name": "greet"
            }
          ],
          "intent": {
            "confidence": 1.0,
            "name": "greet"
          },
          "entities": []
        },
        "event": "user",
        "text": "/greet"
      }
    ]
  },
  "arguments": {},
  "template": "utter_greet",
  "channel": {
    "name": "collector"
  }
}
```

然后，端点需要使用生成的响应进行响应：

```
{
    "text": "hey there",
    "buttons": [],
    "image": null,
    "elements": [],
    "attachments": []
}
```

然后，Rasa 将使用此响应并将其发送回用户。

## 5. Actions

```
Actions是机器人为响应用户输入二运行的内容，Rasa中有四种Actions:
1. Utterance actions: 以utter_开头，并向用户发送特定消息
2. Retrieval actions: 以response_开头，并发送一个检索(retrieval)模型选择的消息
3. Custom actions: 运行任意代码并发送任意数量的消息（或无）
4. Default actions: 例如action_listen, action_restart, action_default_fallback
```

### 5.1 Utterance actions（话语操作）

```
要定义话语操作（ActionUtterTemplate），请将话语模板添加到以utter_列开头的域文件中：

templates:
  utter_my_message:
    - "this is what I want my action to say!"


通常以utter_开始话语操作的名称，如果缺少此前缀，您仍然可以在自定义操作中使用该模板，但无法直接将模板预测为其自己的操作。

如果使用外部 NLG 服务，则无需在域中指定模板，但仍需要将话语名称添加到域的操作列表中。
```

### 5.2 Retrieval actions（检索操作）

```
检索操作可以更轻松地处理大量类似的意图，如闲聊和常见问题解答
```

### 5.3 Custom actions（自定义操作）

```
操作可以运行所需的任何代码。自定义操作可以打开指示灯、向日历添加事件、检查用户的银行余额或您能想象到的任何其他操作。

Rasa 将在预测自定义操作时调用您可以指定的终结点。此终结点应该是一个 Web 服务器，它响应此调用，运行代码并选择性地返回信息以修改对话状态。

若要指定，操作服务器使用 ：endpoints.yml
action_endpoint:
  url: "http://localhost:5055/webhook"
  
并使用 将其传递给脚本。--endpoints endpoints.yml
```

**用python编写的自定义操作**

```
对于用python编写的操作，rasa有一个方便的SDK，它可以为您启动此操作服务器。

您的操作服务器唯一需要安装的是：rasa-sdk (pip install rasa-sdk)
```

```
包含自定义操作的文件应称为 actions.py。或者，可以使用名为actions的包目录，或者手动指定带有--actions标志的操作模块或包。

如果已安装，请运行以下命令以启动操作服务器：rasa
rasa run actions

否则，如果尚未安装，请运行以下命令：rasa
python -m rasa_sdk --actions actions
```

```python
'''
在餐厅机器人中，如果用户说“向我展示墨西哥餐厅”，机器人可以执行ActionCheckRestaurants操作，这可能如下所示：
'''
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionCheckRestaurants(Action):
   def name(self) -> Text:
      return "action_check_restaurants"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

      cuisine = tracker.get_slot('cuisine')
      q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
      result = db.query(q)

      return [SlotSet("matches", result if result is not None else [])]
```

```
应将操作名称action_check_restaurants添加到域文件中的操作中。操作的run方法接收三个参数。您可以访问插槽的值和用户使用tracker发送的最新消息，并且可以通过调用dispatcher.utter_message()将消息发送回具有dispatcher对象的用户。

run()方法的详细信息：
Action.run()
@param:  dispatcher -> 将消息发送回用户的调度程序。使用dipatcher.utter_message()或者rasa_sdk.executor.CollectingDispatcher方法
		 tracker    -> 当前用户的状态跟踪器，可以使用tracker.get_slot(slot_name)访问槽值(slot value)，最新的用户消息是tracker.latest_message.text和任何其他rasa_sdk.Tracker属性
		 domain     ->
@return: 返回实例的字典，即rasa_sdk.events.Event，通过endpoint返回
@return type: List[Dict[str, Any]]
```

### 5.4 在其他代码中执行操作

```
Rasa 将向您的服务器发送一个 HTTP POST请求，其中包含有关要运行哪个操作的信息。此外，此请求将包含有关对话的所有信息。操作服务器显示详细的 API 规范。

作为对Rasa的操作调用的响应，您可以修改跟踪器，例如通过设置插槽并将响应发送回用户。所有修改都是使用事件完成的。事件中有一个所有可能的事件类型的列表。
```

### 5.5 使用action主动与用户联系

```
您可能希望主动联系用户，例如，显示长时间运行的后台操作的输出或通知用户外部事件。

为此，您可以到此终结点 ，指定应在请求正文中为特定用户运行的操作。使用查询参数指定应使用哪个输出通道将助手的响应传达给用户。如果邮件是静态的，则可以使用相应的模板在域文件中定义操作。如果需要更多控制，请在域中添加自定义操作，并在操作服务器中实现所需的步骤。在自定义操作中调度的任何消息都将转发到指定的输出通道。POSToutput_channelutter_

主动联系用户取决于渠道的能力，因此并非每个渠道都支持。如果您的频道不支持它，请考虑使用回调输入通道将消息发送到 Webhook。
```

### 5.6 默认操作

| 八个默认操作                     | 说明                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| `action_listen`                  | 停止预测更多操作并等待用户输入。                             |
| `action_restart`                 | 重置整个对话。如果映射策略包含在策略配置中，可以在会话期间通过输入`/restart`来触发。 |
| `action_default_fallback`        | 撤消最后一条用户消息（就好像用户没有发送它并且机器人没有反应一样），并说出机器人不理解的消息。 |
| `action_deactivate_form`         | 停用活动表单并重置请求的插槽。                               |
| `action_revert_fallback_events`  | 还原在 TwoStageFallbackPolicy 期间发生的事件。               |
| `action_default_ask_affirmation` | 要求用户确认其意图。建议使用自定义操作覆盖此默认操作，以获得更有意义的提示。 |
| `action_default_ask_rephrase`    | 要求用户重新表述其意图。                                     |
| `action_back`                    | 撤消最后一条用户消息（就好像用户没有发送它并且机器人没有反应一样）。如果策略配置中包含映射策略，则可以在会话期间通过输入来触发。`/back` |

```
可以覆盖所有默认操作。为此，请将操作名称添加到您域中的操作列表中：
actions:
- action_default_ask_affirmation
然后，Rasa 将调用你的操作终结点，并将其视为所有其他自定义操作。
```

## 6. Policies

### 6.1 配置策略

```
rasa.core.policies.Policy类决定在对话的每一步都要采取什么操作。

有不同的策略可供选择，您可以在单个 rasa.core.agent.Agent.Agent 中包含多个策略。

默认情况下，代理在每次用户消息发送后最多可以预测 10 个后续操作。要更新此值，您可以将环境变量MAX_NUMBER_OF_PREDICTIONS设置为所需的最大预测数。

项目文件config.yml需要一个密钥，您可以使用policies密钥来自定义助手使用的策略。在下面的示例中，最后两行演示如何使用自定义策略类并向其传递参数。
```

```yaml
policies:
  - name: "KerasPolicy"
    featurizer:
    - name: MaxHistoryTrackerFeaturizer
      max_history: 5
      state_featurizer:
        - name: BinarySingleStateFeaturizer
  - name: "MemoizationPolicy"
    max_history: 5
  - name: "FallbackPolicy"
    nlu_threshold: 0.4
    core_threshold: 0.3
    fallback_action_name: "my_fallback_action"
  - name: "path.to.your.policy.class"
    arg1: "..."
```

#### 最大历史记录

```
Rasa Core 策略的一个重要超参数是 max_history.这控制了模型查看的对话历史记录量，以决定接下来要执行的操作。

您可以通过将其传递到策略配置 yaml 文件中策略的Featurizer来设置 max_history。

例如，假设您有一个描述偏离主题的用户消息的out_of_scope意图。如果机器人连续多次看到此意图，则可能需要告诉用户你可以为他们提供哪些帮助。所以你的故事可能看起来像这样：

* out_of_scope
   - utter_default
* out_of_scope
   - utter_default
* out_of_scope
   - utter_help_message
   
   
对于 Rasa Core 要学习此模式，max_history必须至少为 4。

如果你增加你的max_history，你的模型会变得更大，训练将花费更长的时间。如果你有一些信息应该影响对话很远的未来，你应该把它存储为一个插槽。插槽信息始终可用于每个功能处理程序。
```

#### 数据扩充

```
训练模型时，默认情况下，Rasa Core 将通过随机将故事文件中的故事粘合在一起来创建更长的故事。这是因为如果你有这样的故事：

# thanks
* thankyou
   - utter_youarewelcome

# bye
* goodbye
   - utter_goodbye
   
你实际上想教你的policy在对话历史不相关时忽略它，无论以前发生过什么，都要用同样的行动来回应。

您可以使用--augmentation标志更改此行为。这允许您设置 augmentation_factor. augmentation_factor确定在训练期间子采样的增强故事数。增强的故事在训练之前被子采样，因为它们的数量很快就会变得非常大，我们想要限制它。采样故事的数量为augmentation_factor x10。默认情况下，扩充设置为 20，最多可生成 200 个扩充故事。

--augmentation 0禁用所有增强行为。基于记忆的策略不受增强（独立于 augmentation_factor）的影响，并且将自动忽略所有增强的故事。
```

### 6.2 