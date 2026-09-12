import re

_STRINGS = {
	'chat_werewolves_killed': {
		'en': 'The werewolves killed {0}.',
		'ru': 'Оборотни убили {0}.',
		'tr': "Kurt adamlar {0}'ı öldürdü."
	},
	'chat_werewolves_killed_toxic': {
		'en': '{0} has been poisoned by the toxic wolf during the day and killed by the werewolves this night.',
		'ru': '{0} был отравлен токсичным оборотнем в прошлый день и убит оборотнями этой ночью.',
		'tr': '{0}, gün içerisinde zehirli kurt tarafından zehirlenmişti ve bu gece kurt adamlar tarafından öldürüldü.'
	},
	'chat_werewolf_frenzy_kill': {
		'en': 'The werewolf frenzy killed {0}.',
		'ru': 'Неистовый оборотень убил {0}.',
		'tr': "Çılgın kurt adam {0}'ı öldürdü."
	},
	'chat_serial_killer_killed': {
		'en': 'The serial killer stabbed {0}.',
		'ru': 'Серийный убийца зарезал {0}.',
		'tr': "Seri katil {0}'ı bıçakladı."
	},
	'chat_cannibal_ate': {
		'en': 'The hungry cannibal ate {0}.',
		'ru': 'Голодный каннибал съел {0}.',
		'tr': "Aç yamyam {0}'ı yedi."
	},
	'chat_corruptor_killed': {
		'en': 'The corruptor killed {0}.',
		'ru': 'Хакер убил {0}.',
		'tr': "Hipnoterapist {0} 'ı öldürdü."
	},
	'chat_evil_detective_killed': {
		'en': 'The evil detective has killed {0}.',
		'ru': 'Злой детектив убил {0}.',
		'tr': "Kötü dedektif {0}'ı öldürdü."
	},
	'chat_instigator_killed': {
		'en': 'The instigator killed {0}.',
		'ru': 'Провокатор убил {0}.',
		'tr': "Elebaşı {0}'ı öldürdü."
	},
	'chat_ghost_lady_bound_killed': {
		'en': '{0} was killed because they were bound to another player they previously protected that now died.',
		'ru': '{0} был убит, потому что он был привязан к другому игроку, которого он спас ранее и который теперь умер.',
		'tr': '{0}, daha önce koruduğu ve şimdi ölen başka bir oyuncuya bağlı olduğu için öldü.'
	},
	'chat_evil_cupid_bound_killed': {
		'en': '{0} died because their bound partner was killed',
		'ru': '{0} умер, потому что их связанный партнёр был убит',
		'tr': '{0} bağlı partneri öldüğü için öldürüldü'
	},
	'chat_evil_cupid_killed': {
		'en': '{0} was killed by the evil cupid',
		'ru': '{0} был убит Злым Купидоном',
		'tr': '{0} kötü çöpçatan tarafından öldürüldü'
	},
	'chat_jelly_werewolf_protected': {
		'en': 'The jelly wolf has saved {0}.',
		'ru': 'Желейный оборотень спас {0}.',
		'tr': "Jelibon kurt {0}'ı kurtardı."
	},
	'chat_player_not_killed': {
		'en': 'Player {0} could not be killed!',
		'ru': 'Игрок {0} не может быть убит!',
		'tr': 'Oyuncu {0} öldürülemez!'
	},
	'chat_the_village_killed': {
		'en': 'The village killed {0}.',
		'ru': 'Жители убили {0}.',
		'tr': "Köy {0}'ı idam etti."
	},
	'chat_judge_has_rightfully_convicted': {
		'en': 'The judge has rightfully convicted and executed {0}.',
		'ru': 'Судья справедливо осудил и казнил {0}.',
		'tr': "Yargıç haklı bir hüküm verdi ve {0}'ı idam etti."
	},
	'chat_judge_has_wrongfully_convicted': {
		'en': 'The judge {0} has wrongfully convicted {1}. They are a villager! The village rioted and killed {0}!',
		'ru': 'Судья {0} неправомерно осудил {1}. Он мирный житель! Деревня взбунтовалась и убила {0}!',
		'tr': "Yargıç {0} haksız yere {1}'e idam hükmü verdi. O bir köylü! Köylüler isyan ederek {0}'ı öldürdü!"
	},
	'chat_jailer_killed_target': {
		'en': 'The jailer executed their prisoner last night. {0} is dead.',
		'ru': 'Тюремщик казнил своего заключённого прошлой ночью. {0} умер.',
		'tr': 'Dün gece gardiyan tutsağını öldürdü. {0} öldü.'
	},
	'chat_gunner_shot': {
		'en': '{0} shot {1}.',
		'ru': '{0} застрелил {1}.',
		'tr': "{0}, {1}'ı vurdu."
	},
	'chat_marksman_shot': {
		'en': 'The marksman has shot {0}.',
		'ru': 'Меткий стрелок сделал выстрел в {0}.',
		'tr': "Nişancı {0} 'ı vurdu."
	},
	'chat_marksman_backfire': {
		'en': '{0} tried to shoot {1} but killed themself! {2} is a villager!',
		'ru': '{0} попытался выстрелить в {1}, но убил сам себя! {2} житель!',
		'tr': "{0}, {1}'ı vurmayı denedi ama kendini öldürdü. {2} bir köylü!"
	},
	'chat_warden_kill': {
		'en': 'The warden gave a weapon to an inmate who used it to kill {0}!',
		'ru': 'Надзиратель дал оружие своему подопечному, который застрелил {0}!',
		'tr': "Koğuş bekçisi, bir mahkuma {0}'ı öldürmek için kullandığı bir silah verdi!"
	},
	'chat_warden_backfire': {
		'en': '{0} tried to kill {1} with a weapon from the warden but the weapon backfired! {1} is a villager!',
		'ru': '{0} попытался убить {1} оружием надзирателя, но пуля отрикошетила обратно! {1} - житель!',
		'tr': "{0}, {1}'i koğuş liderinden aldığı silahla öldürmeye çalıştı ancak silah geri tepti! {1} bir köylü."
	},
	'chat_warden_werewolves_killed': {
		'en': '{0} jailed two werewolves. The werewolves broke out of their prison and killed the warden!',
		'ru': '{0} посадил в карцер двух оборотней. Они, не долго думая, сбежали из заточения и застрелили надзирателя!',
		'tr': '{0}, 2 tane kurt adamı hapse attı. Kurt adamlar hapishaneden kaçtılar ve koğuş bekçisini öldürdüler!'
	},
	'chat_vigilante_shot': {
		'en': '{0} shot {1}.',
		'ru': '{0} выстрелил в {1}.',
		'tr': "{0}, {1}'i vurdu.\n\n"
	},
	'chat_vigilante_reveal': {
		'en': 'The vigilante has revealed {0}.',
		'ru': 'Линчеватель раскрыл роль {0}.',
		'tr': "Kanunsuz, {0}'ın rolünü açığa çıkardı.\n"
	},
	'chat_priest_use_holy_water_killed': {
		'en': '{0} has thrown holy water at and killed {1}.',
		'ru': '{0} кинул святую воду и убил {1}.',
		'tr': "{0} zemzem suyunu kullandı ve {1}'ı öldürdü."
	},
	'chat_priest_use_holy_water_commit_suicide': {
		'en': '{0} has thrown holy water at {1} and killed themself. {2} is not a werewolf!',
		'ru': '{0} кинул святую воду в {1} и убил сам себя. {2} не оборотень!',
		'tr': '{0} zemzem suyunu {1} üzerinde kullandı ve kendisini öldürdü. {2} kurt adam değil!'
	},
	'chat_bully_killed': {
		'en': '{0} threw a rock at {1} who was already concussed, killing them.',
		'ru': '{0} бросил камень в {1} и убил его, так как он был уже без сознания.',
		'tr': "{0} zaten beyin sarsıntısı geçiren {1}'e taş attı ve onu öldürdü."
	},
	'chat_zombie_bitten_converted_zombie': {
		'en': '{0} is now a zombie.',
		'ru': '{0} теперь зомби.',
		'tr': '{0} artık bir zombi.'
	},
	'chat_player_surrendered': {
		'en': '{0} has fled from the village.',
		'ru': '{0} сбежал из деревни.',
		'tr': '{0} köyden kaçtı.'
	},
	'chat_message_winner_village': {
		'en': 'The village wins!',
		'ru': 'Жители победили!',
		'tr': 'Köy kazandı!'
	},
	'chat_message_winner_werewolves': {
		'en': 'The werewolves win!',
		'ru': 'Оборотни победили!',
		'tr': 'Kurt adamlar kazandı!'
	},
	'chat_message_winner_solo': {
		'en': '{0} wins. They are the {1}!',
		'ru': '{0} победил. Он {1}!',
		'tr': '{0} kazandı. O {1}!',
		'_word_slots': {1}
	},
	'chat_message_winner_sect': {
		'en': 'The sect wins!',
		'ru': 'Секта победила!',
		'tr': 'Tarikat kazandı!'
	},
	'chat_message_winner_zombie': {
		'en': 'The zombies win!',
		'ru': 'Зомби победили!',
		'tr': 'Zombiler kazandı!'
	},
	'chat_message_winner_lovers': {
		'en': 'The lovers win!',
		'ru': 'Любовники победили!',
		'tr': 'Aşıklar kazandı!'
	},
	'chat_message_winner_bandit': {
		'en': 'The bandit and their accomplice(s) win!',
		'ru': 'Бандит и его сообщник(и) победили!',
		'tr': 'Haydut ve suç ortakları kazandı!'
	},
	'chat_message_winner_tie': {
		'en': 'Game ended in a tie. There are no winners.',
		'ru': 'Игра закончилась ничьей. Здесь нет победителей.',
		'tr': 'Oyun berabere bitti. Kazanan yok.'
	},
	'role_shapeshifter_killed': {
		'en': 'The shapeshifter killed {0} and shapeshifted into their role!',
		'ru': 'Лицемер убил {0} и вжился в его роль!',
		'tr': "Taklitçi {0}'ı öldürdü ve onun kılığına girdi!"
	},
	'role_arsonist_player_ignited': {
		'en': 'The arsonist set {0} on fire!',
		'ru': 'Поджигатель поджёг {0}!',
		'tr': "Kundakçı {0}'ı yaktı!"
	},
	'role_bomber_player_exploded': {
		'en': '{0} was killed by an explosion!',
		'ru': '{0} был убит взрывом!',
		'tr': '{0} patlamada öldü!'
	},
	'role_astronomer_meteor_shower': {
		'en': 'The astronomer summoned a meteor shower on {0} and killed them.',
		'ru': 'Астроном вызвал метеоритный дождь на {0} и убил его.',
		'tr': 'Gök bilimci {0} oyuncusunun üzerine bir meteor yağmuru çağırdı ve onu öldürdü.'
	},
	'role_harlot_visit_die': {
		'en': '{0} visited an evil player and died.',
		'ru': '{0} посетил злого игрока и умер.',
		'tr': '{0} kötü bir oyuncuyu ziyaret etti ve öldü.'
	},
	'role_harlot_visit_target_die': {
		'en': '{0} visited a player who was attacked and got killed.',
		'ru': '{0} посетил игрока, который был атакован и убит.',
		'tr': '{0} saldırılmış bir oyuncuyu ziyaret etti ve öldü.'
	},
	'role_tough_guy_died': {
		'en': 'Player {0} was wounded last night and has died now.',
		'ru': 'Силач {0} был ранен прошлой ночью и теперь погиб.',
		'tr': 'Sert adam {0} dün gece yaralandı ve bugün öldü.'
	},
	'role_stubborn_werewolf_died': {
		'en': 'Player {0} was wounded and has died now.',
		'ru': 'Игрок {0} был ранен и сейчас погибнет.',
		'tr': 'Oyuncu {0} yaralandı ve şimdi öldü.'
	},
	'role_junior_werewolf_target_killed': {
		'en': "The junior werewolf's death has been avenged, {0} is dead!",
		'ru': 'Смерть малыша оборотня была отомщена, {0} погиб!',
		'tr': 'Yavru kurt adamın ölümünün intikamı alındı, {0} öldü!'
	},
	'role_split_wolf_killed': {
		'en': '{0} was killed because they bounded their soul to another player that died.',
		'ru': '{0} погиб из-за смерти игрока, к душе которого он был привязан.',
		'tr': '{0} ruhunu bağladığı oyuncu öldüğü için öldürüldü.'
	},
	'role_split_wolf_target_killed': {
		'en': '{0} was killed because their soul was bound to a split wolf that died.',
		'ru': '{0} погиб из-за смерти двойственного оборотня, который был привязан к его душе.',
		'tr': '{0} ruhunu bağladığı ayrık kurt öldüğü için öldürüldü.'
	},
	'split_wolf_revealed': {
		'en': '{0} had their role revealed because they bound their themselves to a player who has died.',
		'ru': 'Роль {0} была раскрыта из-за того, что он связал себя с умершим игроком.',
		'tr': "{0}'ın ruhunu bağladığı oyuncu öldüğü için rolü açığa çıktı."
	},
	'role_medium_revived_player': {
		'en': 'The medium revived {0}.',
		'ru': 'Медиум воскресил {0}.',
		'tr': 'Medyum {0} canlandırdı.'
	},
	'role_ritualist_revived_player': {
		'en': 'The ritualist revived {0}.',
		'ru': 'Некромант воскресил {0}.',
		'tr': "Ayinci {0}'ı canlandırdı.\n"
	},
	'role_mayor_reveal_msg': {
		'en': 'Player {0} is the mayor!',
		'ru': 'Игрок {0} - мэр!',
		'tr': 'Oyuncu {0} belediye başkanlığını açığa çıkardı!'
	},
	'role_preacher_reveal_msg': {
		'en': 'Player {0} is the preacher! They will now get extra votes.',
		'ru': 'Игрок {0} - проповедник! Теперь он может воспользоваться дополнительными голосами.',
		'tr': 'Oyuncu {0} hatip! Şimdi fazladan oya sahip olacak.'
	},
	'fortune_teller_card_used_chat_message': {
		'en': "{0} used the fortune teller's card to reveal their role.",
		'ru': '{0} использовал карту гадалки, чтобы раскрыть свою роль.',
		'tr': '{0} falcının kartını rolünü açıklamak için kullandı.'
	},
	'hero_public_announcement_short': {
		'en': 'Player {1} has heroically taken the place of {0}!',
		'ru': 'Игрок {1} героически занял место {0}!',
		'tr': "Oyuncu {1} kahramanca bir şekilde {0}'ın yerini aldı!"
	},
	'weather_rain_washes_off_disguise_chat_message': {
		'en': 'The pouring rain revealed the role of {0}!',
		'ru': 'Проливной дождь раскрыл роль {0}!',
		'tr': "Şiddetli yağmur {0}'ın rolünü açığa çıkardı!"
	},
	'assassins_conference_immunity_winner': {
		'en': "{0} has won last night's puzzle and now has a {1}! The solution was {2}.",
		'ru': '{0} выиграл вчерашнюю головоломку и теперь имеет {1}! Решение было {2}.',
		'tr': "{0} dün gecenin yapbozunu çözdü ve şimdi bir {1}'ı var! Cevap {2}'dı."
	},
	'assassins_conference_no_immunity_winner': {
		'en': "No player has won last night's puzzle! The solution was {0}.",
		'ru': 'Ни один игрок не выиграл вчерашнюю головоломку! Решением было {0}.',
		'tr': "Dün gecenin yapbozunu kimse çözemedi! Cevap {0}'dı."
	},
	'blight_chat_infection_propagated': {
		'en': '{0} has interacted with {1} and is now infected as well.',
		'ru': '{0} взаимодействовал с {1} и теперь также заражен.',
		'tr': '{0}, {1} ile etkileşti ve şu an o da enfekte oldu.'
	},
	'blight_chat_infection_propagated_self': {
		'en': 'You interacted with {0} who has been infected by the blight. You are now also infected.',
		'ru': 'Ты взаимодействовал с {0}, который был заражен вредителем. Теперь ты также заражен.',
		'tr': 'Vebalı tarafından enfekte olmuş {0} ile etkileşime girdin. Sen de enfekte oldun.'
	},
	'blight_chat_player_not_infected': {
		'en': '{0} could not be infected!',
		'ru': '{0} не может быть заражен!',
		'tr': '{0} enfekte edilemedi!'
	},
	'blight_chat_self_infected': {
		'en': 'You have been infected by the blight. The infection will spread to other players who check or reveal your role.',
		'ru': 'Ты был заражен вредителем. Инфекция распространится на других игроков, которые проверят или раскроют твою роль.',
		'tr': 'Vebalı tarafından enfekte edildin. Senin kontrol eden veya rolünü açığa çıkartan oyunculara enfeksiyon yayılacak.'
	},
	'chat_admirer_protection_activated': {
		'en': 'You have activated protection for your target. The next kill attempt on them will be blocked.',
		'ru': 'Ты активировал защиту для своей цели. Следующая попытка убить её будет заблокирована.',
		'tr': 'Hedefin üzerinde koruma aktifleştirdin. Onun üzerinde bir sonraki saldırı engellenecek.'
	},
	'chat_admirer_protection_blocked_kill': {
		'en': 'Your protection saved your target from death!',
		'ru': 'Твоя защита спасла твою цель от смерти!',
		'tr': 'Koruman hedefini ölümden kurtardı!'
	},
	'chat_anarchist_lynchless': {
		'en': 'The village has failed to lynch anyone while evil is still rampant. Anarchy is on the rise. You are one step closer to winning ({0} of {1}).',
		'ru': 'Деревня не смогла казнить кого либо, пока зло бушует. Анархия растёт. Ты на один шаг ближе к победе ({0} из {1}).',
		'tr': "Kötülük hala yaygınken köy kimseyi idam edemedi. Anarşi yükselişte. Kazanmaya bir adım daha yaklaştın ({1}'e {0})."
	},
	'chat_anarchist_miskill': {
		'en': 'The village killed an innocent villager. Unrest is increasing! You can skip the next voting phase.',
		'ru': 'Деревня убила невинного жителя. Беспорядки растут! Ты сможешь отменить следующую фазу голосования.',
		'tr': 'Köy masum bir köylüyü öldürdü. Huzursuzluk artıyor! Sıradaki oylama aşamasını atlayabilirsin.'
	},
	'chat_anarchist_mislynch': {
		'en': 'The village lynched an innocent villager. Unrest is increasing! You can skip the next voting phase.',
		'ru': 'Деревня казнила невинного жителя. Беспорядки растут! Ты можешь отменить следующую фазу голосования.',
		'tr': 'Köy masum bir köylüyü idam etti. Huzursuzluk artıyor! Bir sonraki oylama aşamasını atlayabilirsin.'
	},
	'chat_auto_report': {
		'en': 'Your action has been automatically reported. If you repeat this behavior your account will be banned.',
		'ru': 'Твое действие было автоматически донесено. Если ты повторишь такое поведение, твоя учетная запись будет заблокирована.',
		'tr': 'Eyleminiz otomatik olarak rapor edildi. Bu davranışı tekrarlarsan hesabın banlanır.'
	},
	'chat_baker_bread_sent': {
		'en': 'The baker has sent you bread. You will have one more vote during the voting phase of this day.',
		'ru': 'Пекарь отправил тебе хлеб. Сегодня на голосовании у тебя будет дополнительный голос.',
		'tr': 'Fırıncı sana bir ekmek gönderdi. Bugün oylama zamanında fazladan 1 oy hakkın olacak.'
	},
	'chat_baker_sent': {
		'en': 'You sent {0} bread, they will have one more vote today.',
		'ru': 'Ты отправил хлеб {0}, сегодня у него будет дополнительный голос.',
		'tr': "{0}'a bir ekmek gönderdin. Bugün oylama zamanında fazladan 1 oy hakkı olacak."
	},
	'chat_bandit_welcome': {
		'en': 'Welcome to the bandit chat. Choose a player you want to kill tonight.',
		'ru': 'Добро пожаловать в чат бандитов. Выбери игрока, которого хочешь убить ночью.',
		'tr': 'Haydut sohbetine hoş geldin. Bu gece öldürmek istediğin oyuncuyu seç.'
	},
	'chat_bellringer_revealed': {
		'en': '{0} has been revealed to you.',
		'ru': '{0} был раскрыт тебе.',
		'tr': '{0} sana açıklandı.'
	},
	'chat_bodyguard_injured': {
		'en': 'You fought off an attack last night and survived. Next time you are attacked you will die.',
		'ru': 'Ты избежал атаки и выжил. В следующий раз, если тебя атакуют, ты умрёшь.',
		'tr': 'Dün gece saldırıya uğradın ama savaşmayı başardın ve kurtuldun. Bir daha saldırıya uğrarsan öleceksin.'
	},
	'chat_bully_concussed': {
		'en': 'A bully threw a rock at you, leaving you concussed. You cannot talk or play until the end of the next phase.',
		'ru': 'Хулиган бросил в тебя камень, в результате чего ты получил сотрясение мозга. Ты не можешь говорить или играть до конца следующей фазы.',
		'tr': 'Bir kabadayı sana taş attı ve seni sarsılmış halde bıraktı. Bir sonraki aşamanın sonuna kadar konuşamaz veya oynayamazsın.'
	},
	'chat_bully_concussed_failed': {
		'en': 'You threw a rock at {0}. However, they have been concussed before by another bully and you were unable to hit them.',
		'ru': 'Ты бросил камень в {0}. Однако, он уже получил сотрясение от другого хулигана, поэтому ничего не произошло.',
		'tr': "{0}'a bir taş attın. Ama daha önce başka bir zorba tarafından sarsıldıkları için ona vuramadın."
	},
	'chat_bully_threw_rock': {
		'en': 'You threw a rock at {0} giving them a concussion.',
		'ru': 'Ты бросил камень в {0} и он получил сотрясение мозга.',
		'tr': "{0}'a taş atarak ona beyin sarsıntısı geçirttin."
	},
	'chat_butcher_fed_used': {
		'en': 'You have fed the werewolves, they will not be able to kill next night.',
		'ru': 'Ты покормил оборотней, они не смогут убить в следующую ночь.',
		'tr': 'Kurt adamları besledin, ertesi gece öldüremeyecekler.'
	},
	'chat_confusion_wolf_hide_night_kills_active': {
		'en': '{0} has activated confusion. The role of players who die tonight will be hidden from non-werewolf players!',
		'ru': '{0} активировал сумбур. Роли игроков, которые умрут этой ночью, будут скрыты от всех не-оборотней!',
		'tr': '{0}, karmaşa yeteneğini kullandı. Bu gece ölecek oyuncuların rolü kurt olmayan herkesten gizlenecek!'
	},
	'chat_conjuror_convert': {
		'en': 'You converted to the role of {0} until the beginning of the next voting phase.',
		'ru': 'Ты превратился в роль {0} до начала следующего голосования.',
		'tr': "Bir sonraki oylama aşamasına kadar {0}'ın rolüne dönüştün."
	},
	'chat_conjuror_convert_back': {
		'en': 'You converted back to your original role of Conjuror.',
		'ru': 'Ты вернулся к своей первоначальной роли Фокусника.',
		'tr': 'Orijinal rolün olan Afsuncuya geri döndün.'
	},
	'chat_conjuror_welcome': {
		'en': 'Welcome conjuror! You can now start talking to the dead!',
		'ru': 'Приветствуем, фокусник! Ты можешь начать разговаривать с мёртвыми!',
		'tr': 'Hoş geldin afsuncu! Şimdi ölülerle konuşmaya başlayabilirsin!'
	},
	'chat_conjuror_will_not_see_dead_chat': {
		'en': 'The conjuror has taken the role of a dead player and will not see any messages in the dead chat this night.',
		'ru': 'Фокусник забрал роль мёртвого игрока и не увидит сообщений в чате мёртвых этой ночью.',
		'tr': 'Afsuncu ölü bir oyuncunun rolünü aldı ve bu gece ölü sohbetindeki mesajları göremeyecek.'
	},
	'chat_day_discussion_intro': {
		'en': 'Day {0} has started. Get ready to discuss!',
		'ru': '{0} день начался. Приготовьтесь к обсуждению!',
		'tr': '{0}. gün başladı. Tartışmaya hazırlan!'
	},
	'chat_day_discussion_intro_today_weather': {
		'en': "Day {0} has started. Today's weather: {1}",
		'ru': 'День {0} начался. Сегодняшняя погода: {1}',
		'tr': '{0}. gün başladı. Bugünün hava durumu: {1}'
	},
	'chat_day_discussion_tie_warning': {
		'en': 'Warning, if nobody dies or is converted today or tonight, the game will end in a tie.',
		'ru': 'Внимание, если никто не умрёт или не обратится этой ночью или этим днём, то игра закончится ничьёй.',
		'tr': 'Uyarı, eğer bugün veya bu gece birisi ölmez veya dönüşmezse oyun berabere bitecektir.'
	},
	'chat_day_voting_changed': {
		'en': 'The number of votes needed to lynch has changed! ({0} votes required)',
		'ru': 'Количество голосов для казни было изменено! (требуется {0} голосов)',
		'tr': 'İdam etmek için gereken oy sayısı değişti! ({0} oy gerekli)'
	},
	'chat_day_voting_intro': {
		'en': 'Get ready to vote! ({0} votes required)',
		'ru': 'Приготовьтесь голосовать! ({0} голосов нужно)',
		'tr': 'Oy vermek için hazırlan! ({0} oy gerekli)'
	},
	'chat_day_voting_skipped': {
		'en': 'There is no voting today ✌️',
		'ru': 'Никакого голосования на сегодня✌️',
		'tr': 'Bugün oylama yapılmayacak ✌️'
	},
	'chat_day_voting_skipped_anarchist': {
		'en': 'The village is in revolt. There is no voting today 😡',
		'ru': 'Деревня затеяла бунт. Никакого голосования на сегодня😡',
		'tr': 'Köy isyan etti. Bugün oylama olmayacak 😡'
	},
	'chat_day_voting_skipped_pacifist': {
		'en': 'The {0} has used their ability. There is no voting today ✌️',
		'ru': 'Пацифист использовал свою способность. Никакого голосования сегодня ✌️',
		'tr': '{0} yeteneğini kullandı. Bugün oylama yok ✌️'
	},
	'chat_deep_sea_terror_killed': {
		'en': '{0} was killed by the deep sea terror',
		'ru': '{0} был убит пучиной',
		'tr': "Van gölü canavarı {0}'ı öldürdü"
	},
	'chat_doctor_protected': {
		'en': 'Your protection saved {0} last night!',
		'ru': 'Твоя защита спасла {0} этой ночью!',
		'tr': 'Koruman sayesinde dün gece {0} kurtarıldı!'
	},
	'chat_evil_cupid_players_bound': {
		'en': 'You have bound {0} and {1} together',
		'ru': 'Ты связал {0} и {1} вместе',
		'tr': "{0} ve {1}'i birbirine bağladın"
	},
	'chat_evil_detective_same_team': {
		'en': 'Your targets {0} and {1} are on the same team. They will not be killed tonight.',
		'ru': 'Выбранные тобой {0} и {1} в одной команде. Они не будут убиты.',
		'tr': 'Seçtiğin {0} ve {1} aynı takımdalar. Bu gece öldürülmeyecekler.'
	},
	'chat_evil_detective_same_team_with_team': {
		'en': 'Your targets {0} and {1} are on the {2} team. They will not be killed tonight.',
		'ru': 'Твои цели {0} и {1} находятся в команде {2}. Они не будут убиты сегодня ночью.',
		'tr': 'Seçtiğin {0} ve {1}, {2} takımında. Onları bu gece öldüremeyeceksin.'
	},
	'chat_evil_wizard_killed': {
		'en': '{0} was killed by the evil wizard',
		'ru': '{0} был убит зловещим волшебником',
		'tr': "Kötü büyücü {0}'ı öldürdü"
	},
	'chat_ferryman_welcome': {
		'en': 'Welcome ferryman! You can now start talking to the dead!',
		'ru': 'Привет, паромщик! Сейчас ты можешь говорить с мертвыми!',
		'tr': 'Hoş geldin kayıkçı! Şimdi ölülerle konuşmaya başlayabilirsin!'
	},
	'chat_flower_child_player_cannot_be_lynched': {
		'en': 'This player cannot be lynched today.',
		'ru': 'Этот игрок не может быть казнён сегодня.',
		'tr': 'Bu oyuncu bugün asılamaz.'
	},
	'chat_flower_child_protected': {
		'en': 'You protected {0} from being lynched.',
		'ru': 'Ты защитил {0} от казни.',
		'tr': '{0} oyuncusunu asılmaktan kurtardın.'
	},
	'chat_gambler_guess_correct': {
		'en': '{0} is part of the {1} team.',
		'ru': '{0} является частью команды {1}.',
		'tr': '{0} {1} takımının bir parçası.'
	},
	'chat_gambler_guess_incorrect': {
		'en': '{0} is not part of the {1} team.',
		'ru': '{0} не является частью команды {1}.',
		'tr': '{0} {1} takımının bir parçası değil.'
	},
	'chat_game_starting_in': {
		'en': 'Game starting in {0} ...',
		'ru': 'Игра начнется через {0} ...',
		'tr': 'Oyun {0} saniye içinde başlıyor...'
	},
	'chat_ghost_lady_player_saved_by_ghost_lady': {
		'en': '{0} scared away your attackers last night.',
		'ru': '{0} отпугнул напавших на тебя прошлой ночью.',
		'tr': 'Saldırı aldın, ama {0} onları korkutup kaçırdı.'
	},
	'chat_ghost_lady_visited_not_protected': {
		'en': 'You visited {0} last night, and they were not attacked.',
		'ru': 'Прошлой ночью ты посетил {0}, он не был атакован.',
		'tr': "Gece {0}'ı ziyaret ettin ve saldırı almadı."
	},
	'chat_ghost_lady_visited_protected': {
		'en': 'You saved {0} last night. They now know your role.',
		'ru': 'Прошлой ночью ты спас {0}. Теперь он знает твою роль.',
		'tr': "Gece {0}'ı kurtardın. Artık senin rolünü biliyor."
	},
	'chat_ghost_lady_visited_protected_bound': {
		'en': 'You saved {0} last night. Your fate is now bound to theirs and you will die when they are killed.',
		'ru': 'Прошлой ночью ты спас {0}. Твоя судьба теперь связана с его судьбой, и ты умрешь, когда он погибнет.',
		'tr': "{0}'ı kurtardın. Artık kaderin ona bağlı ve o öldüğünde sen de öleceksin."
	},
	'chat_ghost_lady_visited_protected_bound_revealed': {
		'en': 'You saved {0} last night. Your fate is now bound to theirs and you will die when they are killed. Your role has been revealed to them.',
		'ru': 'Прошлой ночью ты спас {0}. Ваши судьбы теперь связаны и ты умрёшь если он умрёт. Ему была раскрыта твоя роль.',
		'tr': "Dün gece {0}'ı kurtardın. Artık kaderin ona bağlı ve o öldürüldüğünde sen de öleceksin. Rolün ona açıklandı."
	},
	'chat_guardian_wolf_protected': {
		'en': 'The guardian wolf protected {0} from being lynched.',
		'ru': 'Волчий страж защитил {0} от казни.',
		'tr': 'Muhafız kurt {0} oyuncusunu asılmaktan kurtardı.'
	},
	'chat_gunner_shot_lose_second_bullet': {
		'en': 'You have shot an innocent member of the village, you have lost your second bullet.',
		'ru': 'Ты выстрелил в невинного жителя и потерял свою вторую пулю.',
		'tr': 'Köyden olan masum birini vurdun, ikinci mermini kaybettin.'
	},
	'chat_host_changed': {
		'en': 'The host has been changed!',
		'ru': 'Произошла замена ведущего!',
		'tr': 'Oda yöneticisi değişti!'
	},
	'chat_host_killed_player': {
		'en': 'Host killed {0}.',
		'ru': 'Ведущий убил {0}.',
		'tr': "Yönetici {0}'ı öldürdü."
	},
	'chat_jailer_jailed_player_is_asleep': {
		'en': 'Looks like this player is in a deep sleep! They will not talk to you!',
		'ru': 'Похоже, этот игрок в глубоком сне! Он не будет говорить с тобой!',
		'tr': 'Görünüşe göre bu oyuncu derin bir uykuda! Seninle konuşmayacak!'
	},
	'chat_jailer_jailed_you': {
		'en': 'You are in jail. Try to convince the jailer that you are innocent.',
		'ru': 'Ты в тюрьме. Попробуй убедить тюремщика в своей невиновности.',
		'tr': 'Şuan hapistesin. Gardiyanı masum olduğuna ikna etmeye çalış.'
	},
	'chat_jailer_successful_jailed': {
		'en': '{0} is in jail. You can now talk privately with each other.',
		'ru': '{0} в тюрьме. Ты можешь лично переговариваться с ним.',
		'tr': '{0} hapiste. Artık onunla gizlice konuşabilirsin.'
	},
	'chat_jelly_werewolf_protected_anonymous': {
		'en': 'The jelly wolf has saved another player.',
		'ru': 'Желейный оборотень спас другого игрока.',
		'tr': 'Jelibon kurt bir oyuncuyu kurtardı.'
	},
	'chat_jelly_wolf_player_cannot_be_killed': {
		'en': 'This player cannot be killed by the village today and tonight.',
		'ru': 'Этот игрок не может быть убит жителями этим днём и следующей ночью.',
		'tr': 'Bu oyuncu bugün ve bu akşam köy tarafından öldürülemez.'
	},
	'chat_joined': {
		'en': '{0} joined.',
		'ru': '{0} присоединился.',
		'tr': '{0} katıldı.'
	},
	'chat_judge_cannot_convict_teammate': {
		'en': '{0} is your teammate! You cannot convict them.',
		'ru': '{0} - твой товарищ по команде! Ты не можешь осудить его.',
		'tr': '{0} senin takım arkadaşın! Ona idam hükmü veremezsin.'
	},
	'chat_judge_your_sentence_was_right': {
		'en': 'Your sentence was right! {0} was not a villager.',
		'ru': 'Твой приговор был правильным! {0} не был мирным жителем.',
		'tr': 'Hükmün doğru! {0} köylü değil.'
	},
	'chat_judge_your_sentence_was_wrong': {
		'en': 'Your sentence was wrong! {0} is a villager.',
		'ru': 'Твой приговор был неверным! {0} - мирный житель.',
		'tr': 'Hükmün yanlış! {0} köylü.'
	},
	'chat_lobby_boost': {
		'en': '{0} boosted the game! Everyone earns +{1}% bonus XP this game.',
		'ru': '{0} активировал улучшение опыта на эту игру! Каждый получит +{1}% бонусного опыта в этом матче.',
		'tr': '{0} oyunu güçlendirdi! Herkes bu oyun fazladan +{1}% XP kazanır.'
	},
	'chat_lobby_boost_anonymous': {
		'en': 'A player boosted the game! Everyone earns +{0}% bonus XP this game.',
		'ru': 'Игрок активировал улучшение опыта на эту игру! Каждый получит +{0}% бонусного опыта в этом матче.',
		'tr': 'Bir oyuncu oyunu güçlendirdi! Herkes bu oyun fazladan +{0}% XP kazanır.'
	},
	'chat_locksmith_broke': {
		'en': 'The lock was broken last night, you are no longer protected.',
		'ru': 'Замок был сломан прошлой ночью, ты больше не защищен.',
		'tr': 'Kilit dün gece kırıldı, artık korunmuyorsun.'
	},
	'chat_locksmith_received': {
		'en': "The locksmith has secured you with their lock, you will be protected as long as you're locked with them.",
		'ru': 'Слесарь запер тебя своим замком, ты будешь защищен, пока заперт им.',
		'tr': 'Çilingir seni kilidiyle korumaya aldı, onunla kilitli olduğun sürece korunacaksın.'
	},
	'chat_locksmith_sent': {
		'en': 'You have locked in {0}, they will be protected.',
		'ru': 'Ты запер {0}, он будет защищен.',
		'tr': "{0}'ı kilitledin, korunacak."
	},
	'chat_medium_welcome': {
		'en': 'Welcome medium! You can now start talking to the dead!',
		'ru': 'Добро пожаловать, медиум! Ты можешь начать разговаривать с умершими!',
		'tr': 'Hoş geldin medyum! Şimdi ölülerle konuşmaya başlayabilirsin!'
	},
	'chat_message_lurker_wins_with_converter_team': {
		'en': '{0} (Lurker) wins together with their converter team.',
		'ru': '{0} (Лазутчик) побеждает с командой, которая его обратила.',
		'tr': '{0} (Aylakçı) onu dönüştüren takımla beraber kazanır.'
	},
	'chat_message_seer_result': {
		'en': 'You checked {0}.',
		'ru': 'Ты проверил {0}.',
		'tr': "{0}'a baktın."
	},
	'chat_message_winner_assassin': {
		'en': 'All hail {0}, the new assassin leader!',
		'ru': 'Да здравствует {0}, новый лидер убийц!',
		'tr': "Yeni suikastçı lideri {0}'a selamlar olsun!"
	},
	'chat_message_winner_assassin_tie': {
		'en': 'There was a tie between {0}. They are now the new assassin leaders!',
		'ru': 'Между {0} была ничья. Теперь они новые лидеры убийц!',
		'tr': '{0} arasında beraberlik vardı. Onlar şimdi yeni suikastçı liderleri!'
	},
	'chat_message_winner_fifth_column': {
		'en': 'The fifth column wins!',
		'ru': 'Пятый столбец победил!',
		'tr': 'Beşinci sütun kazandı!'
	},
	'chat_message_winner_fifth_row': {
		'en': 'The fifth row wins!',
		'ru': 'Пятый ряд победил!',
		'tr': 'Beşinci sıra kazandı!'
	},
	'chat_message_winner_first_column': {
		'en': 'The first column wins!',
		'ru': 'Первый столбец победил!',
		'tr': 'Birinci sütun kazandı!'
	},
	'chat_message_winner_first_row': {
		'en': 'The first row wins!',
		'ru': 'Первый ряд победил!',
		'tr': 'İlk sıra kazandı!'
	},
	'chat_message_winner_fourth_column': {
		'en': 'The fourth column wins!',
		'ru': 'Четвёртый столбец победил!',
		'tr': 'Dördüncü sütun kazandı!'
	},
	'chat_message_winner_fourth_row': {
		'en': 'The fourth row wins!',
		'ru': 'Четвертый ряд победил!',
		'tr': 'Dördüncü sıra kazandı!'
	},
	'chat_message_winner_instigators': {
		'en': 'Instigators win!',
		'ru': 'Провокаторы победили!',
		'tr': 'Elebaşı ve fedaileri kazandı!'
	},
	'chat_message_winner_president_killed': {
		'en': 'The president was killed!',
		'ru': 'Президент был убит!',
		'tr': 'Başkan öldürüldü!'
	},
	'chat_message_winner_second_column': {
		'en': 'The second column wins!',
		'ru': 'Второй столбец победил!',
		'tr': 'İkinci sütun kazandı!'
	},
	'chat_message_winner_second_row': {
		'en': 'The second row wins!',
		'ru': 'Второй ряд победил!',
		'tr': 'İkinci sıra kazandı!'
	},
	'chat_message_winner_third_column': {
		'en': 'The third column wins!',
		'ru': 'Третий столбец победил!',
		'tr': 'Üçüncü sütun kazandı!'
	},
	'chat_message_winner_third_row': {
		'en': 'The third row wins!',
		'ru': 'Третий ряд победил!',
		'tr': 'Üçüncü sıra kazandı!'
	},
	'chat_message_wolf_paci_revealed': {
		'en': 'The {0} has revealed {1} to the werewolf team.',
		'ru': '{0} раскрыл {1} команде оборотней.',
		'tr': "{0}, kurt adam takımına {1}'i açığa çıkardı."
	},
	'chat_message_you_revealed_role_private': {
		'en': 'You have revealed the role of {0}. Only you can see this.',
		'ru': 'Ты раскрыл роль {0}. Только ты можешь это видеть.',
		'tr': "{0}'ın rolünü açığa çıkardın. Bunu sadece sen görebilirsin."
	},
	'chat_message_your_role_was_revealed': {
		'en': 'Your role has been revealed to everyone!',
		'ru': 'Твоя роль была раскрыта для всех!',
		'tr': 'Rolün herkese açıklandı!'
	},
	'chat_message_your_role_was_revealed_inc_role': {
		'en': 'You were revealed as a {0} to everyone!',
		'ru': 'Ты был раскрыт как {0} всем!',
		'tr': 'Herkese {0} olarak açıklandın!'
	},
	'chat_message_your_role_was_revealed_private': {
		'en': 'Your role has been revealed to the {0}.',
		'ru': 'Твоя роль была раскрыта {0}.',
		'tr': "Rolün {0}'a açıklandı."
	},
	'chat_msg_rose_for_you': {
		'en': '{0} has sent you a rose 🌹',
		'ru': '{0} отправил тебе розу 🌹',
		'tr': '{0} sana bir gül gönderdi 🌹'
	},
	'chat_msg_rose_for_you_multiple': {
		'en': '{0} has sent you {1} roses 🌹',
		'ru': '{0} отправил тебе {1} роз(ы) 🌹',
		'tr': '{0} sana {1} gül gönderdi 🌹'
	},
	'chat_msg_rose_from_you': {
		'en': 'You have sent {0} a rose 🌹',
		'ru': 'Ты отправил {0} розу 🌹',
		'tr': "{0}'a bir gül yolladın 🌹"
	},
	'chat_msg_rose_from_you_multiple': {
		'en': 'You have sent {0} {1} roses 🌹',
		'ru': 'Ты отправил {0} {1} роз(ы) 🌹',
		'tr': "{0}'a {1} gül gönderdin 🌹"
	},
	'chat_msg_roses_for_all': {
		'en': '{0} has sent a rose to everybody! 🌹🌹🌹',
		'ru': '{0} отправил всем по розе! 🌹🌹🌹',
		'tr': '{0} herkese bir gül gönderdi! 🌹🌹🌹'
	},
	'chat_msg_roses_for_all_multiple': {
		'en': '{0} has sent {1} roses to everybody! 🌹🌹🌹',
		'ru': '{0} отправил всем {1} роз(ы)! 🌹',
		'tr': '{0} herkese {1} gül gönderdi! 🌹🌹🌹'
	},
	'chat_player_and_player_are_speaking': {
		'en': '{0} and {1} are speaking ...',
		'ru': '{0} и {1} говорят...',
		'tr': '{0} ve {1} konuşuyor...'
	},
	'chat_player_and_player_are_typing': {
		'en': '{0} and {1} are typing ...',
		'ru': '{0} и {1} печатают...',
		'tr': '{0} ve {1} yazıyor...'
	},
	'chat_player_is_speaking': {
		'en': '{0} is speaking ...',
		'ru': '{0} говорит...',
		'tr': '{0} konuşuyor...'
	},
	'chat_player_is_typing': {
		'en': '{0} is typing ...',
		'ru': '{0} печатает...',
		'tr': '{1} yazıyor...'
	},
	'chat_player_left': {
		'en': '{0} left.',
		'ru': '{0} вышел.',
		'tr': '{0} ayrıldı.'
	},
	'chat_player_not_lynched_cause_protection': {
		'en': 'The village tried to lynch {0} but they were protected.',
		'ru': 'Жители пытались казнить {0}, но он был защищен.',
		'tr': "Köy {0}'ı asmayı denedi ama o korundu."
	},
	'chat_players_are_speaking': {
		'en': '{0} players are speaking ...',
		'ru': '{0} игроков говорят...',
		'tr': '{0} oyuncu konuşuyor...'
	},
	'chat_players_are_typing': {
		'en': '{0} players are typing ...',
		'ru': '{0} игроков печатают...',
		'tr': '{1} oyuncu yazıyor...'
	},
	'chat_preacher_extra_vote': {
		'en': 'The villagers have mistakenly lynched one of their own! You get an additional permanent vote.',
		'ru': 'Жители нечаянно казнили одного из своих! Ты навсегда получаешь дополнительный голос.',
		'tr': 'Köylüler yanlışlıkla kendilerinden birini astı! Ek bir kalıcı oy kazandın.'
	},
	'chat_preacher_use_extra_votes': {
		'en': "You used your extra votes, you will have an additional {0} vote(s) during today's voting phase.",
		'ru': 'Ты использовал свои дополнительные голоса, у тебя будет на {0} голоса(-ов) больше на сегодняшнем голосовании.',
		'tr': 'Fazladan oy haklarını kullandın, bugünkü oylama aşamasında ek {0} oy hakkın olacak.'
	},
	'chat_protection_stolen': {
		'en': 'Your protection on {0} was stolen by a snatcher wolf!',
		'ru': 'Твоя защита игрока {0} была украдена волчьим вором!',
		'tr': '{0} üstündeki koruman bir hırsız kurt tarafından çalındı!'
	},
	'chat_public_welcome': {
		'en': 'Welcome to another {0} game. We are glad that you are here :) There are {1} players online, {2} in this language!',
		'ru': 'Добро пожаловать в очередную игру в {0}. Мы рады, что ты здесь :) В сети сейчас {1} человек. {2} на этом языке!',
		'tr': 'Başka bir {0} oyununa hoş geldin. Burada olmana sevindik :) Şu anda {1} kişi çevrim içi, {2} kişi aynı dilde!'
	},
	'chat_public_welcome_advance_game': {
		'en': 'Welcome to a new advanced game! There are currently {0} players online, playing advanced games in your language!',
		'ru': 'Приветствуем в новом режиме многознающих! Сейчас {0} игроков в сети, играющих на твоём языке!',
		'tr': 'Yeni bir gelişmiş oyuna hoş geldiniz! Şu an senin dilinde gelişmiş oyun oynayan {0} çevrimiçi oyuncu var!'
	},
	'chat_public_welcome_game_mode': {
		'en': 'Welcome to another {0} game. We are glad that you are here :) There are {1} players online in this game mode!',
		'ru': 'Добро пожаловать в очередную игру в {0}. Мы рады, что ты здесь :) В этот режим сейчас играют {1} человек!',
		'tr': 'Başka bir {0} oyununa hoş geldin. Burada olmana sevindik :) Şu anda {1} kişi bu oyun modunda çevrim içi!'
	},
	'chat_public_welcome_to_ranked': {
		'en': 'Welcome to a new ranked game! There are {0} players in your skill range online. You are playing: {1}',
		'ru': 'Добро пожаловать в новую ранговую игру! В твоем диапазоне навыка {0} игроков онлайн. Лига этой игры - {1}.',
		'tr': 'Yeni bir dereceli oyununa hoş geldin! Beceri alanında {0} çevrimiçi oyuncu var. Bu bir {1} oyunudur.'
	},
	'chat_ritualist_welcome': {
		'en': 'Welcome ritualist! You can now start talking to the dead!',
		'ru': 'Доброй ночи, некромант! Теперь ты можешь начать говорить с мёртвыми!',
		'tr': 'Hoş geldin ayinci! Artık ölülerle konuşmaya başlayabilirsin!'
	},
	'chat_skip_discussion_count': {
		'en': 'All but {0} voted to skip the discussion phase.',
		'ru': 'Все, кроме {0}, проголосовали за пропуск обсуждения.',
		'tr': '{0} kişi hariç herkes tartışma zamanını geçmek için oy verdi.'
	},
	'chat_skip_discussion_someone_voted': {
		'en': 'Somebody voted to skip the discussion phase.',
		'ru': 'Кто-то проголосовал за пропуск обсуждения.',
		'tr': 'Biri tartışma aşamasını atlamak için oy verdi.'
	},
	'chat_snatcher_wolf_protection_used': {
		'en': 'A player was saved by stolen protection!',
		'ru': 'Игрок был защищён украденной защитой!',
		'tr': 'Bir oyuncu çalınan bir korumayla kurtarıldı!'
	},
	'chat_snatcher_wolf_steal_success': {
		'en': 'You successfully stole protection from {0}!',
		'ru': 'Ты успешно украл защиту у {0}!',
		'tr': "{0}'dan başarıyla koruma çaldın!"
	},
	'chat_spam_warning': {
		'en': 'You are spamming the chat. Please be nice to other players.',
		'ru': 'Ты спамишь в чате. Пожалуйста, будь добр к другим игрокам.',
		'tr': 'Sürekli mesaj gönderiyorsun. Lütfen diğer oyunculara iyi davran.'
	},
	'chat_spectator_joined': {
		'en': '{0} joined the spectators.',
		'ru': '{0} присоединился к зрителям.',
		'tr': '{0} seyircilere katıldı.'
	},
	'chat_spy_are_not_suspects': {
		'en': 'Your observation has revealed that none of your targets have killed last night.',
		'ru': 'Твоё наблюдение показало, что никто из твоих целей не убивал прошлой ночью.',
		'tr': 'Gözlemin hedeflerinin dün gece kimseyi öldürmediğini ortaya çıkardı.'
	},
	'chat_spy_are_suspects': {
		'en': 'Your observation has revealed that one of your targets has killed last night.',
		'ru': 'Твоё наблюдение показало, что одна из твоих целей убивала прошлой ночью.',
		'tr': 'Gözlemin hedeflerinden birinin dün gece birini öldürdüğünü ortaya çıkardı.'
	},
	'chat_spy_is_not_villager': {
		'en': "{0} doesn't belong to the village.",
		'ru': '{0} - не житель.',
		'tr': '{0} köyden değil.'
	},
	'chat_spy_is_villager': {
		'en': '{0} is part of the village.',
		'ru': '{0} - житель.',
		'tr': '{0} köyün yerlisi.'
	},
	'chat_spy_not_enough_suspects': {
		'en': 'You did not select enough suspects last night to conduct the observation.',
		'ru': 'Ты не выбрал достаточно подозреваемых, чтобы провести наблюдение.',
		'tr': 'Gözlemi gerçekleştirmek için yeteri kadar şüpheli seçmedin.'
	},
	'chat_storm_wolf_swapped': {
		'en': 'The storm wolf has shuffled all players!',
		'ru': 'Громовой оборотень поменял местами всех игроков!',
		'tr': 'Fırtına kurt, tüm oyuncuların yerini değiştirdi!'
	},
	'chat_very_bad_word': {
		'en': 'You have used inappropriate language which is not tolerated. Please be nice to other players.',
		'ru': 'Ты использовал ненормативную лексику, которая не допускается.  Пожалуйста, будь добр к другим игрокам.',
		'tr': 'Hoş görülmeyen uygunsuz bir dil kullandın. Lütfen diğer oyunculara iyi davran.'
	},
	'chat_village_no_lynch': {
		'en': 'The village could not decide who to lynch.',
		'ru': 'Жители не решили, кого казнить.',
		'tr': 'Köy kimi idam edeceğine karar veremedi.'
	},
	'chat_vote_change_host': {
		'en': '{0} voted to change the host.',
		'ru': '{0} проголосовал за смену ведущего.',
		'tr': '{0} oda yöneticisinin değişmesi için oy verdi.'
	},
	'chat_voting_intro_final': {
		'en': 'Get ready for the final vote! Dead players vote who they think played the best and should win the game. Dead chat is enabled for the rest of the game.',
		'ru': 'Приготовьтесь к финальному голосованию! Мертвые игроки голосуют за того, кто, по их мнению, сыграл лучше всех и заслуживает победу. Чат мёртвых включен до конца игры.',
		'tr': 'Son oy için hazır ol! Ölü oyuncular en iyisi olup kazanmayı hak ettiğini düşündüğü oyuncuya oy verebilir. Ölü sohbeti oyunun geri kalanı için açık.'
	},
	'chat_voting_intro_no_min': {
		'en': 'Get ready to vote!',
		'ru': 'Приготовьтесь голосовать!',
		'tr': 'Oylamak için hazırlan!'
	},
	'chat_voting_intro_tie': {
		'en': 'Get ready for a tie-breaker! The next tie will result in a random player being killed.',
		'ru': 'Приготовьтесь к тай-брейку! Следующая ничья приведет к тому, что случайный игрок будет убит.',
		'tr': 'Beraberlik bozma oylamasına hazır ol! Sıradaki beraberlik rastgele bir oyuncunun öldürülmesiyle sonuçlanacak.'
	},
	'chat_warden_cannot_break_out': {
		'en': 'You tried to break out, but the warden cannot be killed this night.',
		'ru': 'Ты попытался сбежать, но надзиратель не может быть убит этой ночью.',
		'tr': 'Hapishaneden kurtulmayı denedin, ama koğuş bekçisi bu gece öldürülemez.'
	},
	'chat_warden_into': {
		'en': 'You have put {0} and {1} into jail. You can listen to their conversation.',
		'ru': 'Ты посадил {0} и {1} в карцер. Ты можешь подслушать их разговор.',
		'tr': "{0} ve {1}'i hapishaneye koydun. Onların konuşmasını dinleyebilirsin."
	},
	'chat_warden_jailed_player_is_asleep': {
		'en': 'Looks like {0} is in a deep sleep! They will not be able to talk this night!',
		'ru': 'Кажется {0} спит как убитый! Похоже, от него не будет толка этой ночью!',
		'tr': 'Görünüşe göre {0} derin bir uykuda! Bu gece konuşamayacak!'
	},
	'chat_warden_werewolves': {
		'en': 'The warden jailed you and another werewolf. You can pretend to be villagers, or break out and kill the warden instead.',
		'ru': 'Надзиратель посадил тебя и другого оборотня в карцер. Вы можете прикинуться жителями или сбежать из карцера и застрелить надзирателя.',
		'tr': 'Koğuş bekçisi seni ve başka bir kurt adamı hapse attı. Köylü gibi davranabilirsiniz ya da kurtulup koğuş bekçisini öldürebilirsiniz.'
	},
	'chat_werewolf_betray': {
		'en': 'It looks like you tried to reveal your werewolf colleagues. This is considered gamethrowing and is not tolerated. Please respect your teammates.',
		'ru': 'Кажется, ты пытался раскрыть роль оборотня, твоего коллеги. Это считается порчей игры и недопустимым. Пожалуйста, уважай членов своей команды.',
		'tr': 'Kurt adam arkadaşlarını ortaya çıkarmaya çalışmışsın. Bu oyunbozanlık olarak kabul edilir ve hoş karşılanmaz. Lütfen takım arkadaşlarına saygı göster.'
	},
	'chat_werewolf_frenzy_active': {
		'en': 'The werewolf berserk activated frenzy for this night!',
		'ru': 'Неистовый оборотень активировал ярость на эту ночь!',
		'tr': 'Çılgın kurt adam bu gece cinnet geçirecek!'
	},
	'chat_werewolf_frenzy_inactive': {
		'en': 'The werewolf berserk was killed and the frenzy has been stopped!',
		'ru': 'Неистовый оборотень был убит, и ярость была остановлена!',
		'tr': 'Çılgın kurt adam öldürüldü ve cinnet durduruldu!'
	},
	'chat_werewolves_night_intro': {
		'en': 'Night {0} has started.',
		'ru': 'Ночь {0} началась.',
		'tr': '{0}. gece başladı.'
	},
	'chat_werewolves_welcome': {
		'en': 'Welcome to the werewolves chat.',
		'ru': 'Добро пожаловать в чат оборотней.',
		'tr': 'Kurt adam sohbetine hoş geldin.'
	},
	'chat_wizard_killed': {
		'en': '{0} was killed by the wizard',
		'ru': '{0} был убит волшебником',
		'tr': '{0}, gulyabani tarafından öldürüldü'
	},
	'chat_wolffluencer_influenced_player': {
		'en': 'You influenced {0} and can manipulate their vote today.',
		'ru': 'Ты повлиял на {0} и можешь управлять его голосом сегодня.',
		'tr': "{0}'ı etkiledin ve bugün onun oyunu manipüle edebilirsin."
	},
	'chat_wolffluencer_vote_manipulated': {
		'en': 'The wolffluencer has influenced a player, they will control their vote today.',
		'ru': 'Влиятельный оборотень повлиял на игрока, сегодня он сможет управлять его выбором на голосовании.',
		'tr': 'Manipülator kurt bir oyuncuyu etkisi altına aldı. Bugünkü oyunu kontrol edecek.'
	},
	'chat_wolffluencer_you_are_influenced': {
		'en': 'The wolffluencer has influenced you, they will control who you vote for today.',
		'ru': 'Влиятельный оборотень повлиял на тебя, сегодня он сможет управлять твоим выбором на голосовании.',
		'tr': 'Manipülatör kurt seni etkisi altına aldı. Bugün kime oy verdiğini kontrol edecek.'
	},
	'chat_zombie_bite_failed': {
		'en': '{0} could not be bitten.',
		'ru': '{0} не может быть укушен.',
		'tr': '{0} ısırılamaz.'
	},
	'chat_zombie_bitten_converted_self': {
		'en': 'You have been bitten and are a zombie now! Happy brain hunting!',
		'ru': 'Ты был укушен и теперь обратился в зомби! Удачной охоты за мозгами!',
		'tr': 'Isırıldın ve artık bir zombisin! Beyin avlamada iyi eğlenceler!'
	},
	'chat_zombie_bitten_self': {
		'en': 'You have been bitten! You will become a zombie the next day.',
		'ru': 'Тебя укусили! На следующий день ты превратишься в зомби.',
		'tr': 'Isırıldın! Ertesi gün bir zombiye dönüşeceksin.'
	},
	'chat_zombie_bitten_zombie': {
		'en': '{0} was bitten last night.',
		'ru': '{0} был укушен прошлой ночью.',
		'tr': '{0} dün gece ısırıldı.'
	},
	'clan_chat_player_joined': {
		'en': '{0} joined your clan!',
		'ru': '{0} вступил в твой клан!',
		'tr': '{0} klanına katıldı!'
	},
	'clan_chat_player_left': {
		'en': '{0} left your clan!',
		'ru': '{0} покинул твой клан!',
		'tr': '{0} klanından ayrıldı!'
	},
	'corruptor_chat_player_not_corrupted': {
		'en': '{0} could not be glitched!',
		'ru': '{0} не может быть взломан!',
		'tr': '{0} hipnotize edilemedi!'
	},
	'event_bunny_killed': {
		'en': 'Hooray, the evil bunny has been defeated! Easter has been saved and everything is back to normal. You poked it {0} times.',
		'ru': 'Наконец, злой пасхальный кролик был побеждён! Деревня была спасена и все вернулось в норму. Ты тыкнул его {0} раз(а).',
		'tr': 'Yaşasın, kötü tavşan yenilgiye uğratıldı! Paskalya kurtarıldı ve her şey normale döndü. Onu {0} kez dürttün.'
	},
	'event_generic_boss_killed': {
		'en': 'Hooray, the monster has been defeated! Everything is back to normal. You poked it {0} times.',
		'ru': 'Наконец, монстр был побеждён! Все вернулось в норму. Ты тыкнул в него {0} раз.',
		'tr': 'Yaşasın, canavar yenilgiye uğratıldı! Her şey normalde döndü. Onu {0} kez dürttün.'
	},
	'event_squid_killed': {
		'en': 'Hooray, the evil squid has been defeated! Everything is back to normal. You poked it {0} times.',
		'ru': 'Наконец, злой осьминог побеждён! Все вернулось в норму. Ты тыкнул в него {0} раз.',
		'tr': 'Yaşasın, kötü kalamar yenilgiye uğratıldı! Her şey normale döndü. Onu {0} kere dürttün.'
	},
	'fortune_teller_card_to_player_chat_message': {
		'en': 'The fortune teller gave you one of their cards.',
		'ru': 'Гадалка отдала тебе одну из своих карт.',
		'tr': 'Falcı sana kartlarından birini verdi.'
	},
	'fortune_teller_card_used_killed_chat_message': {
		'en': "{0} was given a card by a fortune teller that was just killed. Since they didn't use the card, their role has been revealed.",
		'ru': '{0} получил карту от гадалки, которая только что была убита. Поскольку они не использовали карту, их роль была раскрыта.',
		'tr': "{0}'a az önce öldürülen bir falcı tarafından bir kart verildi. Kartı kullanmadığı için rolü açığa çıktı."
	},
	'game_evil_wizard_role_blocked': {
		'en': 'You have been role blocked by the Evil Wizard.',
		'ru': 'Твоя роль была заблокирована зловещим волшебником.',
		'tr': 'Kötü Büyücü tarafından yeteneklerin engellendi.'
	},
	'game_wizard_killed_player': {
		'en': '{0} was killed by the wizard for not obeying the command.',
		'ru': '{0} был убит волшебником за неподчинение его воле.',
		'tr': '{0}, gulyabani tarafından ona itaat etmediğinden dolayı öldürüldü.'
	},
	'game_wizard_role_blocked': {
		'en': 'You have been role blocked by the Wizard for not obeying.',
		'ru': 'Твоя роль была заблокирована волшебником за неподчинение.',
		'tr': 'Gulyabaniye itaat etmediğinden dolayı onun tarafından bu gecelik yeteneklerin engellendi.'
	},
	'hero_public_announcement': {
		'en': 'Player {1} has heroically taken the place of {0}! It might take them some time to understand the state of the game so please be nice!',
		'ru': 'Игрок {1} героически занял место {0}! У него может уйти некоторое время, чтобы понять, что происходит в игре, будьте вежливы!',
		'tr': "Oyuncu {1} kahramanca bir şekilde {0}'ın yerini aldı! Oyunun durumunu anlaması biraz zaman alabilir, o yüzden ona karşı lütfen nazik olun!"
	},
	'hot_potato_killed_player': {
		'en': 'The bomb exploded and killed {0}.',
		'ru': 'Бомба взорвалась и убила {0}.',
		'tr': "Bomba patladı ve {0}'ı öldürdü."
	},
	'illusionist_chat_player_not_deluded': {
		'en': '{0} could not be disguised!',
		'ru': '{0} не может быть замаскирован!',
		'tr': '{0} gizlenemez!'
	},
	'kitten_wolf_chat_conversion_active': {
		'en': '{0} is dead! This night, instead of picking a player to kill you vote for a player to turn into a werewolf.',
		'ru': '{0} мертв! Этой ночью вместо убийства игрока, вы голосуете за того, кто обратится в оборотня.',
		'tr': '{0} öldü! Bu gece, bir oyuncuyu öldürmek yerine, kurt adama dönüşmesi için oy vereceksin.'
	},
	'kitten_wolf_chat_failed': {
		'en': 'You tried to convert {0} without success.',
		'ru': 'Ты безуспешно попытался превратить {0}.',
		'tr': "{0}'ı dönüştürmekte başarısız oldun."
	},
	'kitten_wolf_chat_success': {
		'en': 'You successfully converted {0}. They are a werewolf now!',
		'ru': 'Ты успешно обратил {0}. Теперь он оборотень!',
		'tr': "{0}'ı başarılı bir şekilde dönüştürdün. O artık bir kurt adam!"
	},
	'kitten_wolf_chat_you_have_been_converted': {
		'en': 'The kitten wolf converted you! You are a werewolf now!',
		'ru': 'Волк-котёнок обратил тебя! Теперь ты оборотень!',
		'tr': 'Kedicik kurt seni dönüştürdü! Artık bir kurt adamsın!'
	},
	'kitten_wolf_chat_you_were_converted': {
		'en': 'In their grief over the loss of the kitten werewolf the werewolves have turned you into one of them!',
		'ru': 'Потеря волка-котенка сказалась на оборотнях. Чтобы компенсировать потерю, они обратили тебя в свою команду!',
		'tr': 'Kurt adamlar, kedicik kurtu kaybetmenin üzüntüsüyle seni kendilerinden biri yaptı.'
	},
	'lobby_chat_drafting_now_picking': {
		'en': 'Now picking: {0}',
		'ru': 'Текущий выбор: {0}',
		'tr': 'Şu an seçiliyor: {0}'
	},
	'lobby_chat_drafting_player_picked': {
		'en': '{0} has drafted {1}.',
		'ru': '{0} выбрал {1}.',
		'tr': '{0}, {1} seçti.'
	},
	'lobby_chat_drafting_started': {
		'en': 'Role drafting has started, get ready to pick a role!',
		'ru': 'Начался выбор ролей, приготовься выбрать роль!',
		'tr': 'Rol seçimi başladı, rol seçmek için hazır ol!'
	},
	'lobby_chat_drafting_started_numbered': {
		'en': 'Role drafting has begun! You are player #{0} in the selection order.',
		'ru': 'Выбор ролей начался! Ты {0} в очереди.',
		'tr': 'Rol seçimi başladı! Seçim sırasında #{0} numaralı oyuncusun.'
	},
	'player_is_blocked_feeding': {
		'en': 'You have been fed by the butcher and are not hungry enough to kill a player this night.',
		'ru': 'Тебя покормил мясник, теперь ты недостаточно голоден, чтобы убить игрока этой ночью.',
		'tr': 'Kasap, seni besledi ve bu gece bir oyuncuyu öldürecek kadar aç değilsin.'
	},
	'player_is_blocked_new_moon': {
		'en': 'A new moon is active, non villagers will not be able to kill tonight.',
		'ru': 'Новолуние активно, никто, кроме жителей, не сможет убивать сегодня ночью.',
		'tr': 'Yeni ay aktif, köylü olmayan oyuncular bu gece öldüremeyecek.'
	},
	'role_alchemist_chat_you_received_a_potion': {
		'en': 'The alchemist has sent you a potion. Sadly, you cannot make out the color... you might die at the end of the discussion phase. ',
		'ru': 'Алхимик дал тебе зелье. К сожалению, ты не можешь разобрать цвет... возможно ты погибнешь в конце этапа обсуждения.',
		'tr': 'Simyacı sana bir iksir gönderdi. Ne yazık ki iksirin rengini anlayamıyorsun... tartışma aşamasının sonunda ölebilirsin.'
	},
	'role_alchemist_kill_failed': {
		'en': '{0} could not be poisoned this night.',
		'ru': '{0} не мог быть отравлен этой ночью.',
		'tr': '{0} bu gece zehirlenemedi.'
	},
	'role_alchemist_killed': {
		'en': 'The alchemist killed {0}.',
		'ru': 'Алхимик убил {0}.',
		'tr': "Simyacı {0}'ı öldürdü."
	},
	'role_analyst_blocked': {
		'en': 'Because they have matching auras, you will not be able to check again next night.',
		'ru': 'Ты не сможешь проверять на следующую ночь из-за того, что у них совпадают ауры.',
		'tr': '. Eşleşen auraları olduğu için sonraki gece tekrar kontrol edemeyeceksin.'
	},
	'role_analyst_result': {
		'en': 'You checked {0} and {1}.',
		'ru': 'Ты проверил {0} и {1}.',
		'tr': "{0} ve {1}'i kontrol ettin"
	},
	'role_arsonist_doused': {
		'en': 'You have doused {0} this night.',
		'ru': 'Ты облил бензином {0} этой ночью.',
		'tr': "Bu gece {0}'a benzin döktün."
	},
	'role_arsonist_not_doused': {
		'en': 'Your target could not be doused.',
		'ru': 'Твоя цель не может быть облита бензином.',
		'tr': 'Hedefinin evine benzin dökemezsin.'
	},
	'role_astronomer_killed_villager': {
		'en': 'The stars were not happy with {0} and avenged {1} who was an innocent villager.',
		'ru': 'Звезды были недовольны {0} и отомстили за невиновного жителя деревни {1}.',
		'tr': 'Yıldızlar {0} ile mutlu değildi ve masum bir köylü olan {1}in intikamını aldı.'
	},
	'role_astronomer_new_moon': {
		'en': 'A new moon is rising. Werewolves cannot kill tonight.',
		'ru': 'Наступает новолунье. Оборотни не смогут убивать сегодня ночью.',
		'tr': 'Yeni ay yükseliyor. Kurt adamlar bu gece öldüremeyecek.'
	},
	'role_avenger_killed_player': {
		'en': 'The avenger has avenged their death and killed {0}!',
		'ru': 'Мститель отомстил за свою смерть и убил {0}!',
		'tr': "İntikamcı ölümünün intikamını aldı ve {0}'ı öldürdü!"
	},
	'role_baker_bread_given': {
		'en': "The baker gave you bread. You have one more vote during today's voting phase.",
		'ru': 'Пекарь дал тебе хлеб. Сегодня у тебя будет дополнительный голос.',
		'tr': 'Fırıncı sana bir ekmek verdi. Bugünkü oylama zamanında fazladan 1 oy hakkın var.'
	},
	'role_baker_sent_fail': {
		'en': "You couldn't send the bread to {0}.",
		'ru': 'Ты не смог отправить хлеб {0}',
		'tr': "{0}'a ekmek gönderemedin."
	},
	'role_bandit_chat_convert_failed': {
		'en': 'You could not convert {0} to be your accomplice last night.',
		'ru': 'Ты не смог сделать {0} своим сообщником ночью.',
		'tr': "Dün gece {0}'ı suç ortağına dönüştüremedin."
	},
	'role_bandit_chat_convert_kill': {
		'en': "{0} didn't want to be your accomplice so you decided to kill them.",
		'ru': 'Игрок {0} не захотел быть твоим сообщником, поэтому ты решил убить его.',
		'tr': '{0} suç ortağın olmak istemedi bu yüzden onu öldürmeye karar verdin.'
	},
	'role_bandit_chat_convert_success': {
		'en': 'You successfully converted {0}. They are now your accomplice!',
		'ru': 'Ты успешно сделал {0} своим сообщником!',
		'tr': "{0}'ı başarıyla dönüştürdün. O artık senin suç ortağın!"
	},
	'role_bandit_chat_converted_you': {
		'en': 'The bandit ({0}) chose you last night to be their accomplice!',
		'ru': 'Бандит ({0}) выбрал тебя своим сообщником!',
		'tr': 'Haydut {0} geçen gece suç ortağı olman için seni seçti!'
	},
	'role_bandit_chat_converted_you_inc_role': {
		'en': 'The bandit ({0}) chose you last night to be their accomplice! You are no longer a {1}.',
		'ru': 'Бандит ({0}) выбрал тебя прошлой ночью своим сообщником! Ты больше не {1}.',
		'tr': 'Haydut ({0}) dün gece suç ortağı olman için seni seçti! Artık bir {1} değilsin.'
	},
	'role_bandit_player_killed': {
		'en': 'The bandits killed {0}.',
		'ru': 'Бандиты убили {0}.',
		'tr': "Haydutlar {0}'ı öldürdü."
	},
	'role_beast_hunter_move_msg': {
		'en': 'The trap is already placed. Moving it will deactivate the trap for this night.',
		'ru': 'Ловушка уже установлена. Перемещение ловушки отключит её на эту ночь.',
		'tr': 'Tuzak zaten yerleştirildi. Eğer tuzağı taşırsan bu gece tuzak devre dışı kalacak.'
	},
	'role_beast_hunter_trap_killed': {
		'en': "The beast hunter's trap killed {0}.",
		'ru': 'Охотничья ловушка убила {0}.',
		'tr': 'Canavar avcısının tuzağı {0} oyuncusunu öldürdü.'
	},
	'role_blight_player_killed': {
		'en': 'The blight killed {0}!',
		'ru': 'Вредитель убил {0}!',
		'tr': "Vebalı {0}'ı öldürdü!"
	},
	'role_candy_wolf_system_kill': {
		'en': 'A candy wolf poisoned {0} the previous night. The victim could have been saved, but no protector was available.',
		'ru': 'Карамельный оборотень отравил {0} прошлой ночью. Жертву можно было спасти, но рядом не оказалось защитника.',
		'tr': "Bir Şeker Kurt dün gece {0}'ı zehirledi. Kurban korunabilirdi, ama yardım eden bir koruyucu yoktu."
	},
	'role_candy_wolf_system_not_poisoned': {
		'en': 'Your target {0} could not be poisoned.',
		'ru': 'Твоя цель {0} не может быть отравлена.',
		'tr': 'Hedefin {0} zehirlenemedi.'
	},
	'role_candy_wolf_system_poisoned': {
		'en': 'You have poisoned {0}. They will be killed at the end of the next night unless they are protected.',
		'ru': 'Ты отравил {0}. Он будет убит в конце следующей ночи, если не будет защищен.',
		'tr': "{0}'ı zehirledin. Korunmazlarsa bir sonraki gece sonu ölecek."
	},
	'role_candy_wolf_system_protected': {
		'en': '{0} was protected this night and survived your poison.',
		'ru': '{0} был защищен этой ночью и пережил твое отравление.',
		'tr': '{0} bu gece korundu ve zehrinden korundu.'
	},
	'role_candy_wolf_system_self_poisoned': {
		'en': 'You have been poisoned. You will die at the end of the night unless you are protected tonight.',
		'ru': 'Ты был отравлен. Ты умрешь в конце ночи, если не будешь защищен в эту ночь.',
		'tr': 'Zehirlendin. Bir koruyucunun yardımını alamazsan bir sonraki gece sonu öleceksin.'
	},
	'role_candy_wolf_system_self_protected': {
		'en': 'You were protected last night and are no longer poisoned.',
		'ru': 'Тебя защитили прошлой ночью и ты больше не отравлен.',
		'tr': 'Dün gece korundun ve artık zehirli değilsin.'
	},
	'role_cannibal_max_eats': {
		'en': 'You cannot get more hungry since you reached the limit of eating {0} players in one night.',
		'ru': 'Ты не можешь стать более голодным, так как достиг предела поедания {0} игроков за одну ночь.',
		'tr': 'Bir gecede {0} oyuncu yeme limitine eriştiğin için daha fazla acıkamazsın.'
	},
	'role_cannot_be_killed_by_werewolves': {
		'en': 'You cannot be killed by the werewolves.',
		'ru': 'Ты не можешь быть убит оборотнями.',
		'tr': 'Kurt adamlar tarafından öldürülemezsin.'
	},
	'role_chat_nutcracker_revealed_role': {
		'en': "{0} is the nutcracker! They have started the 'Final march,' ensuring two players face justice at the end of the day!",
		'ru': "{0} - Щелкунчик! Он начал 'Финальный марш', гарантируя, что двух игроков в конце дня настигнет правосудие!",
		'tr': "{0} Fındıkkıran! Günün sonunda iki oyuncuya adalet sağlamak için 'Son Yürüyüş'ü emretti!"
	},
	'role_chat_pumpkin_dealer_deal_declined': {
		'en': "You declined the pumpkin dealer's offer.",
		'ru': 'Ты отклонил предложение торговца тыквами.',
		'tr': 'Balkabağı tüccarının teklifini reddettin.'
	},
	'role_chat_pumpkin_dealer_deal_outcome_bullet': {
		'en': "The pumpkin dealer's deal granted you a bullet.",
		'ru': 'Сделка с тыквенным крупье принесла тебе пулю.',
		'tr': 'Balkabağı tüccarının teklifi sana bir mermi verdi.'
	},
	'role_chat_pumpkin_dealer_deal_outcome_bullet_already_owned': {
		'en': "The pumpkin dealer's deal gave you a bullet, but you already had one. You still only have one bullet.",
		'ru': 'Тыквенный крупье дал тебе пулю, но у тебя уже была одна. У тебя по-прежнему одна пуля.',
		'tr': 'Balkabağı tüccarının teklifi sana bir mermi verdi, ama sende zaten bir tane vardı. Yine bir mermin olacak.'
	},
	'role_chat_pumpkin_dealer_deal_outcome_nothing': {
		'en': "The pumpkin dealer's deal had no effect.",
		'ru': 'Сделка тыквенного крупье не оказала никакого эффекта.',
		'tr': 'Balkabağı tüccarının teklifi bir etki vermedi.'
	},
	'role_chat_pumpkin_dealer_deal_outcome_protection': {
		'en': "The pumpkin dealer's deal will protect you tonight.",
		'ru': 'Тыквенный крупье будет защищать тебя этой ночью.',
		'tr': 'Balkabağı tüccarının teklifi bu gece seni koruyacak.'
	},
	'role_chat_pumpkin_dealer_deal_outcome_roleblock': {
		'en': "The pumpkin dealer's deal has role-blocked you tonight.",
		'ru': 'Тыквенный крупье заблокировал твою роль на эту ночь.',
		'tr': 'Balkabağı tüccarının teklifi yüzünden bu gece yeteneklerini kullanamayacaksın.'
	},
	'role_chat_pumpkin_dealer_protection_saved': {
		'en': "The pumpkin dealer's protection saved you last night!",
		'ru': 'Защита тыквенного крупье спасла тебя прошлой ночью!',
		'tr': "Balkabağı tüccarı'nın koruması dün gece seni kurtardı!"
	},
	'role_chat_pumpkin_dealer_sent_you_deal': {
		'en': 'The pumpkin dealer has sent you a deal offer. You can accept or decline during the day phase.',
		'ru': 'Тыквенный крупье отправил тебе предложение о сделке. Ты можешь принять его или отклонить в течении дня.',
		'tr': 'Balkabağı tüccarı sana bir anlaşma teklifi gönderdi. Gün içinde kabul veya reddedebilirsin.'
	},
	'role_chat_time_traveler_game_reset': {
		'en': 'A time traveler has reset the state of the game',
		'ru': 'Путешественник во времени сбросил состояние игры',
		'tr': 'Bir zaman yolcusu oyunu geriye aldı'
	},
	'role_chat_time_traveler_game_resetting': {
		'en': 'A time traveler has used their ability, the game is about to reset back to the start of the previous day.',
		'ru': 'Путешественник во времени использовал свою способность – игра скоро вернётся к началу предыдущего дня.',
		'tr': 'Bir zaman yolcusu yeteneğini kullandı, oyun bir önceki günün başına geri alınacak.'
	},
	'role_cowardly_lion_not_enough_villagers': {
		'en': 'Not enough villagers are alive to make your final stand worthwhile.',
		'ru': 'Недостаточно жителей в живых, чтобы твой последний бой имел смысл.',
		'tr': 'Son duruşunu değerli kılmak için yeterince yaşayan köylü yok.'
	},
	'role_cowardly_lion_token_earned': {
		'en': 'You found a little more courage. You now have {0} saved.',
		'ru': 'Ты обрёл немного уверенности. Теперь у тебя {0} смелости.',
		'tr': 'Biraz daha cesaretin oldu. Artık {0} cesaretin var.'
	},
	'role_cowardly_lion_tokens_spent': {
		'en': 'The Cowardly Lion roars from beyond the grave, casting {1} extra votes against {0}!',
		'ru': 'Трусливый Лев ревёт прямиком из могилы, направляя {1} дополнительных голосов против {0}!',
		'tr': "Korkak Aslan mezarın altından kükreyerek {0}'a karşı {1} oy veriyor!"
	},
	'role_cupid_show_lover_msg': {
		'en': 'You are in love with {0}. You win if you stay alive together until the end of the game. You die if your lover dies.',
		'ru': 'Ты и {0} - любовники. Ты выиграешь, если ты и твой любовник останетесь живы до конца игры. Ты умрёшь, если твой любовник погибнет.',
		'tr': "{0}'a aşıksın. Oyunun sonuna kadar birlikte hayatta kalırsanız kazanırsın. Sevgilin ölürse sen de ölürsün."
	},
	'role_cupid_surrender': {
		'en': 'Player {0} lost the love of their life and fled the village!',
		'ru': 'Игрок {0} лишился любви всей своей жизни и сбежал из деревни!',
		'tr': 'Oyuncu {0} hayatının aşkını kaybetti ve köyden kaçtı!'
	},
	'role_cursed_human_converted_self': {
		'en': 'You have been bitten! You are a werewolf now!',
		'ru': 'Тебя укусили! Теперь ты оборотень!',
		'tr': 'Isırıldın! Artık bir kurt adamsın!'
	},
	'role_cursed_human_converted_ww': {
		'en': '{0} was cursed and has been converted into a werewolf!',
		'ru': '{0} оказался проклятым и теперь обращён в оборотня!',
		'tr': '{0} lanetliydi ve kurt adama dönüştü!'
	},
	'role_deep_sea_terror_marked_cannot_vote': {
		'en': 'You have been captured by the deep sea terror! You cannot vote during the day.',
		'ru': 'Ты был захвачен пучиной! Ты не можешь голосовать этим днём.',
		'tr': 'Van gölü canavarı tarafından yakalandın! Gündüzleri oy vermeyeceksin.'
	},
	'role_detective_team_different': {
		'en': '{0} and {1} have a different team!',
		'ru': '{0} и {1} играют за разные команды!',
		'tr': '{0} ve {1} farklı takımda!'
	},
	'role_detective_team_equal': {
		'en': '{0} and {1} have the same team!',
		'ru': '{0} и {1} играют за одну и ту же команду!',
		'tr': '{0} ve {1} aynı takımda!'
	},
	'role_dorothy_crew_completed': {
		'en': 'You have gathered brains, a heart, and courage. You can now throw your bucket of water at any player, but only once.',
		'ru': 'Ты собрал ум, сердце и смелость. Теперь ты можешь швырнуть ведро воды в любого игрока, но лишь единожды.',
		'tr': 'Bir beyin, kalp ve cesaret topladın. Artık istediğin bir oyuncuya istediğin zaman su fırlatabilirsin ama sadece bir kere.'
	},
	'role_dorothy_found_brain': {
		'en': 'You visited {0} and found brains. They have an information ability.',
		'ru': 'Ты посетил {0} и нашёл ум. У этого игрока информационная способность.',
		'tr': "{0}'ı ziyaret ettin ve bir beyin buldun. Onun bir bilgilendirme yeteneği var."
	},
	'role_dorothy_found_courage': {
		'en': 'You visited {0} and found courage. They have a killing ability.',
		'ru': 'Ты посетил {0} и нашёл смелость. У этого игрока убивающая способность.',
		'tr': "{0}'ı ziyaret ettin ve bir cesaret buldun. Onun bir öldürme yeteneği var."
	},
	'role_dorothy_found_heart': {
		'en': 'You visited {0} and found a heart. They have a protection ability.',
		'ru': 'Ты посетил {0} и нашёл сердце. У этого игрока защитная способность.',
		'tr': "{0}'ı ziyaret ettin ve bir kalp buldun. Onun bir koruma yeteneği var."
	},
	'role_dorothy_throw_water_killed': {
		'en': '{0} was killed by a splash of water.',
		'ru': '{0} был убит всплеском воды.',
		'tr': '{0}, fırlatılan bir su tarafından öldürüldü.'
	},
	'role_dorothy_throw_water_no_kill': {
		'en': 'Your water washed harmlessly off {0}. The bucket is empty.',
		'ru': 'Твоя вода стекла с {0}, не нанеся вреда. Ведро опустело.',
		'tr': "Suyun zararsızca {0}'ı ıslattı. Su kovan boş."
	},
	'role_dorothy_visit_uncategorized': {
		'en': 'You visited {0}, but they have nothing to offer.',
		'ru': 'Ты посетил {0}, но у него ничего не было.',
		'tr': "{0}'ı ziyaret ettin ama sana verebilecekleri bir özellik yok."
	},
	'role_easter_bunny_aura_result': {
		'en': 'You sense that {0} has an aura.',
		'ru': 'Ты чувствуешь, что у игрока {0} есть аура.',
		'tr': '{0} aurasının olduğunu hissediyorsun.'
	},
	'role_easter_bunny_blue_egg': {
		'en': 'You shared your blue egg with {0}. They are role-blocked tonight.',
		'ru': 'Ты поделился синим яйцом с игроком {0}. Его роль будет заблокирована на эту ночь.',
		'tr': 'Mavi yumurtanı {0} ile paylaştın. O, bu gece yeteneklerini kullanamayacak.'
	},
	'role_easter_bunny_chat_you_received_an_egg': {
		'en': 'The Easter bunny has sent you an egg! Check out your inventory, you have a new "Easter bunny" front item!',
		'ru': 'Пасхальный кролик послал тебе яйцо! Проверь свой инвентарь, ты получил новый передний фон "Пасхальный кролик"!',
		'tr': 'Paskalya tavşanı sana bir yumurta gönderdi! Envanterini kontrol et, yeni bir "Paskalya Tavşanı" ön öğen var!'
	},
	'role_easter_bunny_egg_wasted': {
		'en': 'You did not select anyone to visit. Your egg was wasted.',
		'ru': 'Ты не выбрал никого для посещения. Твоё яйцо было утрачено.',
		'tr': 'Ziyaret etmek için kimseyi seçmedin. Yumurtan boşa gitti.'
	},
	'role_easter_bunny_golden_egg': {
		'en': 'You shared your golden egg with {0}. You are both protected tonight.',
		'ru': 'Ты поделился золотым яйцом с игроком {0}. Этой ночью вы оба защищены.',
		'tr': 'Altın yumurtanı {0} ile paylaştın. Bu gece ikiniz de korunacaksınız.'
	},
	'role_easter_bunny_red_egg': {
		'en': 'You shared your red egg and sensed the aura of {0}.',
		'ru': 'Ты поделился красным яйцом и почувствовал ауру игрока {0}.',
		'tr': 'Kırmızı yumurtanı {0} ile paylaştın ve aurasını hissettin.'
	},
	'role_easter_bunny_visit_saved': {
		'en': 'You were visiting another player and avoided an attack on you.',
		'ru': 'Ты посетил другого игрока и избежал атаки.',
		'tr': 'Başka bir oyuncuyu ziyaret ediyordun ve sana yapılan saldırıdan kaçtın.'
	},
	'role_easter_bunny_white_egg': {
		'en': 'You shared your white egg with {0}. You will both be muted tomorrow.',
		'ru': 'Ты поделился белым яйцом с игроком {0}. Завтра вы оба будете заглушены.',
		'tr': 'Beyaz yumurtanı {0} ile paylaştın. Yarın ikiniz de susturulacaksınız.'
	},
	'role_evil_santa_killed': {
		'en': '{0} received a deadly gift from the evil santa last night and died.',
		'ru': '{0} получил смертельный подарок от Злого Санты прошлой ночью и умер.',
		'tr': '{0} kötü noel babadan bir ölümcül hediye aldı ve öldü.'
	},
	'role_ferryman_player_wounded': {
		'en': 'Player {0} had their death delayed by a Ferryman this night. They will die at the start of the next night.',
		'ru': 'Паромщик отсрочил кончину игрока {0} этой ночью. Он умрет в начале следующей ночи.',
		'tr': "Oyuncu {0}'ın ölümü bir Kayıkçı tarafından geciktirildi. Bir sonraki gecenin başında ölecek."
	},
	'role_ferryman_wounded_killed': {
		'en': 'Player {0} has succumbed to the wounds inflicted by a {1} the previous night.',
		'ru': 'Игрок {0} скончался от ран, нанесенных {1} прошлой ночью.',
		'tr': 'Oyuncu {0} bir önceki gece {1} tarafından açılan yaralara yenik düştü.'
	},
	'role_ferryman_wounded_killed_wo_killer': {
		'en': 'Player {0} has succumbed to the wounds inflicted the previous night.',
		'ru': 'Игрок {0} скончался от ран нанесенных ему прошлой ночью.',
		'tr': 'Oyuncu {0} bir önceki gece aldığı yaralara yenik düştü.'
	},
	'role_firework_wolf_system_kill': {
		'en': 'The firework wolf gave {0} a send-off to remember, sparks, smoke, and all.',
		'ru': 'Волк-Пиротехник устроил для {0} незабываемые проводы с искрами, дымом и всеми спецэффектами.',
		'tr': "Havai fişek kurt {0}'ı patlamalar, kıvılcımlar, dumanlar ve anılarla uğurladı."
	},
	'role_flagger_players_selected': {
		'en': '{0} will be protected, and {1} will be attacked instead.',
		'ru': '{0} будет защищен, а {1} вместо него будет атакован.',
		'tr': '{0} korunacak ve {1} onun yerine saldırıya uğrayacak.'
	},
	'role_flagger_redirect_attack': {
		'en': 'An attack was redirected by the flagger!',
		'ru': 'Атака была перенаправлена ​​Флагманом!',
		'tr': 'Bir saldırı işaretçi tarafından yönlendirildi!'
	},
	'role_flagger_redirect_kill': {
		'en': 'An attack was redirected to {0} by the flagger!',
		'ru': 'Атака была перенаправлена ​​на {0} флагманом!',
		'tr': "Bir saldırı işaretçi tarafından {0}'a yönlendirildi!"
	},
	'role_flagger_redirection_used': {
		'en': 'You successfully redirected an attack from {0} to {1} last night.',
		'ru': 'Вчера ночью ты успешно перенаправил атаку с {0} на {1}.',
		'tr': "Dün gece bir saldırıyı {0}'dan {1}'e başarıyla yönlendirdin."
	},
	'role_forger_chat_give_failed': {
		'en': 'You could not give your item to {0}.',
		'ru': 'Ты не можешь отдать свой предмет {0}.',
		'tr': "Öğeni {0}'a veremedin."
	},
	'role_forger_chat_given_shield': {
		'en': 'You gave {0} a shield, they will be protected from one attack.',
		'ru': 'Ты отдал щит {0}, он будет защищён от одной атаки.',
		'tr': "{0}'a kalkan verdin, bir saldırıdan korunacak."
	},
	'role_forger_chat_given_sword': {
		'en': 'You gave {0} a sword, they can use it to kill someone.',
		'ru': 'Ты отдал меч {0}, он может использовать его, чтобы убить кого-то.',
		'tr': "{0}'a kılıç verdin, kılıcı birini öldürmek için kullanabilecek."
	},
	'role_forger_chat_received_shield': {
		'en': 'The forger gave you a shield! This will protect you once from being killed at night!',
		'ru': 'Кузнец отдал тебе щит! Он спасёт тебя от смерти однажды ночью!',
		'tr': 'Demirci sana bir kalkan verdi! Bu seni gece bir defa öldürülmekten kurtaracak!'
	},
	'role_forger_chat_received_shield_used': {
		'en': "You have been attacked but the forger's shield saved your life.",
		'ru': 'Ты был атакован, но щит кузнеца спас твою жизнь.',
		'tr': "Saldırıya uğradın ama Demirci'nin kalkanı hayatını kurtardı."
	},
	'role_forger_chat_received_sword': {
		'en': 'The forger gave you a sword! You can use this sword to kill a player.',
		'ru': 'Кузнец отдал тебе меч! Ты можешь использовать его, чтобы убить игрока.',
		'tr': 'Demirci sana bir kılıç verdi! Bu kılıcı birini öldürmek için kullanabilirsin.'
	},
	'role_forger_chat_sword_killed': {
		'en': "The forger's sword was used to kill {0}.",
		'ru': 'Меч кузнеца был использован, чтобы убить {0}.',
		'tr': "Demircinin kılıcı {0}'ı öldürmek için kullanıldı."
	},
	'role_forger_night_view_shield': {
		'en': 'You forged a shield!',
		'ru': 'Ты выковал щит!',
		'tr': 'Bir kalkan oluşturdun!'
	},
	'role_forger_night_view_sword': {
		'en': 'You forged a sword!',
		'ru': 'Ты выковал меч!',
		'tr': 'Bir kılıç oluşturdun!'
	},
	'role_ghost_wolf_is_dead_but_still_can_vote': {
		'en': 'At least one Ghost Wolf is dead, but they can still vote during the voting phase! Their vote is hidden, be careful ...',
		'ru': 'По крайней мере один Призрачный Волк мёртв, но они все еще могут голосовать во время этапа голосования! Их голоса спрятаны, будь аккуратен...',
		'tr': 'En az bir Hayalet Kurt öldü, ama hala oylama aşamasında oy verebilirler! Oyları gizlidir, dikkatli ol...'
	},
	'role_grave_robber_converted_ww': {
		'en': '{0} is a Grave robber and took over the role of {1}.',
		'ru': '{0} - Расхититель гробниц, и он перенял роль {1}.',
		'tr': "{0} bir Mezar hırsızı ve {1}'in rolünü aldı."
	},
	'role_grave_robber_stole_role': {
		'en': 'Your target died. You are now a {0}.',
		'ru': 'Твоя цель умерла. Теперь ты {0}',
		'tr': "Hedefin öldü. Şu anda {0}'sın."
	},
	'role_harlot_visit_die_private': {
		'en': 'You visited {0} last night and they killed you.',
		'ru': 'Ты посетил {0} прошлой ночью и был убит им.',
		'tr': 'Dün gece {0} oyuncusunu ziyaret ettin ve o seni öldürdü.'
	},
	'role_harlot_visit_saved': {
		'en': 'Someone tried to kill you last night.',
		'ru': 'Кто-то пытался убить тебя этой ночью.',
		'tr': 'Önceki gece birisi seni öldürmeyi denedi.'
	},
	'role_headless_horseman_lynchable': {
		'en': 'All werewolves have died. The headless horseman can now be lynched!',
		'ru': 'Все оборотни умерли. Всадника без головы теперь можно казнить!',
		'tr': 'Başı olmayan birini asmak onu öldürmez, ama öfkesine bir son verir. Başsız süvari şuandan itibaren oylanabilir!'
	},
	'role_headless_horseman_system_kill': {
		'en': 'The headless horseman killed {0} last night.',
		'ru': 'Всадник без головы убил {0} прошлой ночью.',
		'tr': "Başsız Süvari dün gece {0}'nın hayatını aldı."
	},
	'role_headless_horseman_system_lynched': {
		'en': 'The villagers tried to lynch {0}. Foolish mortals, you cannot hang someone who has no head!',
		'ru': 'Деревня пыталась линчевать {0}. Глупые смертные, вы не можете повесить того, у кого нет головы!',
		'tr': "Köy {0}'ı asmaya çalıştı. Aptal ölümlüler, başı olmayan birisini asamazsınız!"
	},
	'role_illusionist_kill_discussion_phase_only': {
		'en': 'You can only kill during the discussion phase!',
		'ru': 'Ты можешь убить только на этапе обсуждения!',
		'tr': 'Sadece tartışma aşamasında öldürebilirsin!'
	},
	'role_illusionist_player_killed': {
		'en': 'The illusionist killed {0}!',
		'ru': 'Иллюзионист убил {0}!',
		'tr': "İllüzyonist {0}'ı öldürdü!"
	},
	'role_instigator_recruit_msg': {
		'en': '{0} is a recruit of the instigator. You win if you stay alive together until the end of the game. If either one of you is killed, the other will lose hope and will flee the village.',
		'ru': '{0} - рекрут провокатора. Ты побеждаешь, если вы оба останетесь в живых до конца игры. Если один из вас будет убит, другой потеряет надужду и сбежит из деревни.',
		'tr': '{0}, elebaşının bir fedaisi. Birlikte oyunun sonuna kadar hayatta kalırsanız kazanırsınız. Biriniz ölürse, diğeri umudunu kaybedip köyden kaçacak.'
	},
	'role_instigator_recruit_msg_public': {
		'en': '{0} was a recruit of the instigator.',
		'ru': '{0} был завербован провокатором.',
		'tr': '{0} elebaşının bir fedaisiydi.'
	},
	'role_instigator_show_recruit_msg': {
		'en': 'You and {0} have been recruited by {1}. You win if you stay alive together until the end of the game. You will die if the other recruit is killed.',
		'ru': 'Ты и {0} были набраны {1}. Вы выиграете, если останетесь вместе в живых до конца игры. Ты умрешь, если другой рекрут будет убит.',
		'tr': 'Sen ve {0}, {1} tarafından işe alındınız. Oyunun sonuna kadar hayatta kalırsanız kazanırsınız. Diğer fedai öldürülürse sen de ölürsün.'
	},
	'role_instigator_surrender': {
		'en': 'Player {0} was a recruit of the instigator and fled the village after another recruit was killed!',
		'ru': 'Игрок {0} был рекрутом провокатора и сбежал из деревни после смерти второго рекрута!',
		'tr': 'Oyuncu {0} elebaşının bir fedaisiydi ve diğer fedai öldürüldükten sonra köyden kaçtı!'
	},
	'role_journalist_investigation_killer_is_in_column_x': {
		'en': 'The killer of {0} is in column {1}!',
		'ru': 'Убийца {0} находится в {1} столбце!',
		'tr': "{0}'in katili {1}. sütunda!"
	},
	'role_journalist_investigation_killer_is_in_row_x': {
		'en': 'The killer of {0} is in row {1}!',
		'ru': 'Убийца {0} находится в {1} ряду!',
		'tr': "{0}'in katili {1}. sırada!"
	},
	'role_journalist_investigation_no_results': {
		'en': 'You could not discover the row or column the killer of {0} is in.',
		'ru': 'Ты не смог обнаружить строку или столбец, в котором находится убийца {0}.',
		'tr': "{0}'in katilinin hangi sırada ya da sütunda olduğunu ortaya çıkaramadın."
	},
	'role_journalist_known_information_msg': {
		'en': 'You have previously investigated the death of {0} with the same cause of death as this player. Unless there are multiple players who could have done this, you will not receive any new information.',
		'ru': 'Ты уже расследовал убийство {0} игроков с такой же причиной смерти, что у этого игрока. Если нет нескольких игроков, кто мог совершить это, ты не получишь никакой новой информации.',
		'tr': "Daha önce bu oyuncuyla aynı ölüm nedenine sahip {0}'ın ölümünü araştırdın. Bunu yapmış olabilecek birden fazla oyuncu olmadığı sürece, yeni bir bilgi alamayacaksın."
	},
	'role_locksmith_move_msg': {
		'en': 'Your lock is already set, moving it will unlock it for the night.',
		'ru': 'Твой замок уже установлен, перемещение разблокирует его на ночь.',
		'tr': 'Kilidini zaten kurdun, kilidi hareket ettirmek gece kilidi açacaktır.'
	},
	'role_loudmouth_chat_message': {
		'en': "The loudmouth's last will was to reveal {0}.",
		'ru': 'Последняя воля крикуна заключалась в том, чтобы раскрыть роль {0}.',
		'tr': "Geveze'nin son arzusu {0}'nin rolünü açığa çıkarmaktı."
	},
	'role_lurker_converted': {
		'en': 'You have been attacked and are now part of the {0} team.',
		'ru': 'Ты был атакован и теперь принадлежишь к команде {0}.',
		'tr': 'Saldırıya uğradın ve artık {0} takımının bir parçasısın.'
	},
	'role_lurker_converted_attacker': {
		'en': 'You have attacked {0}. They are a lurker and are now part of your team!',
		'ru': 'Ты атаковал {0}. Он был лазутчиком и теперь с тобой в одной команде!',
		'tr': "{0}'a saldırdın. O bir aylakçı ve artık takımının bir parçası!"
	},
	'role_lurker_converted_village': {
		'en': '{0} has been attacked and is now part of the village team!',
		'ru': '{0} был атакован и стал жителем!',
		'tr': '{0} saldırıya uğradı ve artık köylü takımının bir parçası!'
	},
	'role_mortician_autopsy_dead_results': {
		'en': 'The autopsy showed that the killer of {0} was {1}.',
		'ru': 'Вскрытие показало, что убийцей {0} был {1}.',
		'tr': "Otopsi, {0}'ın katilinin {1} olduğunu ortaya çıkardı."
	},
	'role_mortician_autopsy_no_results': {
		'en': 'The autopsy of {0} did not yield any results.',
		'ru': 'Вскрытие {0} не принесло результатов.',
		'tr': "{0} 'ın otopsisi herhangi bir sonuç vermedi."
	},
	'role_mortician_autopsy_results': {
		'en': 'The autopsy showed that the killer of {2} was {0} or {1}!',
		'ru': 'Вскрытие показало, что убийцей {2} был {1} или {0}!',
		'tr': "Otopsi, {2}'nin katilinin {0} veya {1} olduğunu gösterdi!"
	},
	'role_mortician_autopsy_results_solo': {
		'en': 'The autopsy showed that the killer of {2} was {0}, {1} or {3}!',
		'ru': 'Вскрытие показало, что убийцей {2} был {1}, {0} или {3}!',
		'tr': "Otopsi, {2}'nin katilinin {0}, {1} veya {3} olduğunu gösterdi!"
	},
	'role_mortician_known_information_msg': {
		'en': 'You have previously performed an autopsy on {0} with the same cause of death as this player. Unless there are multiple players who could have done this, you will not receive any new information.',
		'ru': 'Ты уже провёл вскрытие на {0} с такой же причиной смерти, что и у выбранного игрока. Кроме случая где это могли сделать несколько игроков, ты не получишь никакой новой информации.',
		'tr': 'Daha önce bu oyuncuyla aynı ölüm sebebiyle ölen {0} üzerinde otopsi yaptın. Bunu yapabilecek birden fazla oyuncu olmadıkça yeni bir bilgi almayacaksın.'
	},
	'role_night_watchman_used_all_protections': {
		'en': 'You have used all of your protections.',
		'ru': 'Ты потратил всю свою защиту.',
		'tr': 'Bütün korumalarını kullandın.'
	},
	'role_pacifist_reveal_shadow_wolf_warning': {
		'en': "A shadow wolf has doubled the werewolf votes for today. Revealing a role now will cancel today's voting and waste their ability!",
		'ru': 'Теневой оборотень удвоил голоса волков на сегодняшнее голосование. Если ты раскроешь свою роль сейчас, это отменит голосование и потратит его способность!',
		'tr': 'Bir gölge kurt bugün için kurt adam oylarını ikiye katladı. Şu an bir rol açıklamak bugünün oyunu iptal edip gölge kurtun yeteneğini boşa harcayacak!'
	},
	'role_pacifist_revealed_chat': {
		'en': 'The pacifist has revealed {0}. There will be no voting today!',
		'ru': 'Пацифист раскрыл роль {0}. Никакого голосования на сегодня!',
		'tr': 'Barışsever {0} adlı oyuncunun rolünü açığa çıkardı. Bugün oylama yapılmayacak!'
	},
	'role_party_wolf_player_killed': {
		'en': '{0} tried to tango with the party wolf but found the dance floor to be their final stage.',
		'ru': '{0} попытался станцевать танго с праздничным оборотнем, но танцпол оказался его конечной остановкой.',
		'tr': '{0} parti kurdu ile tango yapmaya çalıştı ancak dans pistini son sahnesi olarak buldu.'
	},
	'role_prayer_player_killed': {
		'en': 'A prayer killed {0}!',
		'ru': 'Молящийся убил {0}!',
		'tr': "Duacı {0}'ı öldürdü!"
	},
	'role_pumpkin_dealer_bullet_killed': {
		'en': "The bullet from a pumpkin dealer's deal was used to kill {0}.",
		'ru': 'Пуля, полученная от тыквенного крупье, была использована для убийства {0}.',
		'tr': "Balkabağı tüccarının teklifinden alınan bir mermi {0}'ı öldürmek için kullanıldı."
	},
	'role_pumpkin_dealer_killed': {
		'en': '{0} accepted a risky deal from the pumpkin dealer and was instantly killed by its consequence.',
		'ru': '{0} принял рисковую сделку от тыквенного крупье и был моментально убит ее последствиями.',
		'tr': '{0} balkabağı tüccarından riskli bir teklif kabul etti ve sonuç olarak aniden öldü.'
	},
	'role_pumpkin_king_bucket_back': {
		'en': 'The candy bucket has been returned to you! There are {0} candies inside. All players who helped trick or treat will receive a gift!',
		'ru': 'Ведёрко с конфетами возвращено тебе! Конфет внутри: {0}. Все игроки, которые помогли в сборе, получат подарок!',
		'tr': "Şeker kovası sana geri döndü! İçinde {0} şeker var. Şaka mı şeker mi'ye yardım eden bütün oyuncular ödül alacak!"
	},
	'role_pumpkin_king_bucket_received': {
		'en': "You received the pumpkin king's candy bucket and added a candy. Either pass it on to another player or send it back to the pumpkin king.",
		'ru': 'Ты получил ведёрко для конфет тыквенного короля и добавил туда конфету. Передай его другому игроку или отправь обратно тыквенному королю.',
		'tr': 'Balkabağı kralının şeker kovasını aldın ve bir şeker ekledin. Ya başka bir oyuncuya kovayı yolla ya da kovayı balkabağı kralına geri gönder.'
	},
	'role_pumpkin_king_bucket_received_already': {
		'en': "You received the pumpkin king's bucket, but you have already added a candy. Pass it to another player or send it back to the pumpkin king.",
		'ru': 'Ты получил ведёрко для конфет тыквенного короля, но ты уже положил туда конфету. Передай его другому игроку или отправь обратно тыквенному королю.',
		'tr': 'Balkabağı kralının kovasını aldın ama önceden şeker eklemiştin. Başka bir oyuncuya kovayı yolla ya da kovayı balkabağı kralına geri gönder.'
	},
	'role_pumpkin_king_bucket_sent': {
		'en': 'The candy bucket was sent to {0}!',
		'ru': 'Ведёрко с конфетами отправлено {0}!',
		'tr': "Şeker kovası {0}'a gönderildi!"
	},
	'role_pumpkin_king_bucket_transfer': {
		'en': '{0} sent the bucket to {1}.',
		'ru': '{0} отправил ведёрко {1}.',
		'tr': "{0}, {1}'e kova gönderdi."
	},
	'role_pumpkin_king_thanks': {
		'en': 'The pumpkin king has sent you a gift for helping them trick or treat. You helped collect {0} candies!',
		'ru': 'Тыквенный король прислал тебе подарок за помощь в сборе сладостей. Ты помог собрать конфет: {0}!',
		'tr': "Balkabağı kralı şaka mı şeker mi'ye yardım ettiğin için sana bir hediye gönderdi. {0} şeker toplayarak yardım ettin!"
	},
	'role_pumpkin_oracle_result_one_team_plural': {
		'en': 'Last night you checked the roles of {0}, {1} and {2}. At least {3} of them are {4}.',
		'ru': 'Прошлой ночью ты проверил роли {0}, {1} и {2}. По крайней мере {3} из них - {4}.',
		'tr': "Dün gece {0}, {1} ve {2}'nin rolüne baktın. En az {3} tanesi {4}."
	},
	'role_pumpkin_oracle_result_one_team_singular': {
		'en': 'Last night you checked the roles of {0}, {1} and {2}. At least {3} of them is {4}.',
		'ru': 'Прошлой ночью ты проверил роли {0}, {1} и {2}. По крайней мере {3} из них - {4}.',
		'tr': "Dün gece {0}, {1} ve {2}'nin rolüne baktın. En az {3} tanesi {4}."
	},
	'role_pumpkin_oracle_result_two_teams': {
		'en': 'Last night you checked the roles of {0}, {1} and {2}. At least {3} of them are {4} and {5} {6}.',
		'ru': 'Прошлой ночью ты проверил роли {0}, {1} и {2}. По крайней мере {3} из них - {4} и {5} {6}.',
		'tr': "Dün gece {0}, {1} ve {2}'nin rolüne baktın. En az {3} tanesi {4} ve {5} {6}."
	},
	'role_pumpkin_oracle_result_two_teams_complete': {
		'en': 'Last night you checked the roles of {0}, {1} and {2}. {3} of them are {4} and {5} {6}.',
		'ru': 'Прошлой ночью ты проверил роли {0}, {1} и {2}. {3} из них - {4} и {5} {6}.',
		'tr': "Dün gece {0}, {1} ve {2}'nin rolüne baktın. En az {3} tanesi {4} ve {5} {6}."
	},
	'role_rainmaker_protected': {
		'en': '{0} was protected from being lynched by your rainstick.',
		'ru': '{0} был защищён от казни твоей дождевой палочкой.',
		'tr': '{0} senin yağmur çubuğun tarafından idam edilmekten korundu.'
	},
	'role_rainmaker_protected_public': {
		'en': "The village agreed to lynch {0}. However, a downpour has appeared out of nowhere. Today's lynch is canceled!",
		'ru': 'Деревня согласилась казнить {0}. Однако, появившийся из ниоткуда ливень отменил сегодняшнюю казнь!',
		'tr': "Köy {0}'ı idam etmeye karar verdi. Ancak bir anda sağanak yağış başladı. Bugünkü idam iptal edildi!"
	},
	'role_santa_chat_you_received_a_gift': {
		'en': 'Santa Claus has sent you a gift! Check out your inventory, you have a new "Santa" front item!',
		'ru': 'Санта Клаус отправил тебе подарок! Проверь свой инвентарь, у тебя есть новый предмет от Санты!',
		'tr': 'Noel Baba sana bir hediye yolladı! Envanterine göz at, yeni bir "Noel" öğen var!'
	},
	'role_santa_send_gift_no_players': {
		'en': 'There are no dead and connected players yet.',
		'ru': 'Пока нет мëртвых и подключенных игроков.',
		'tr': 'Şu anda ölmüş ve oyunda olan bir oyuncu yok.'
	},
	'role_scarecrow_torn_bar_used': {
		'en': 'You already survived an attack. You will not survive another one.',
		'ru': 'Ты уже пережил атаку. Вторая станет последней.',
		'tr': 'Zaten bir saldırıdan kurtuldun. Bir sonrakinde öleceksin.'
	},
	'role_scarecrow_torn_night_text': {
		'en': 'You are torn to shreds and cannot observe anyone tonight.',
		'ru': 'Ты порван в клочья и не можешь наблюдать за кем-то этой ночью.',
		'tr': 'Paramparça olduğun için bu gece kimseyi izleyemezsin.'
	},
	'role_sect_leader_converted_by_sect_leader': {
		'en': 'The sect leader converted you last night. You belong to the sect team now!',
		'ru': 'Лидер секты обратил тебя прошлой ночью. Теперь ты играешь за секту!',
		'tr': 'Tarikat lideri dün gece seni tarikatına aldı. Artık tarikat takımındansın!'
	},
	'role_sect_leader_max_members_sacrifice': {
		'en': 'You can only have five sect members at once! You can either sacrifice one to kill another player, or go back to sleep.',
		'ru': 'В секте может одновременно быть не больше пяти игроков! Либо выбери жертву, чтобы убить другого игрока, либо иди спать.',
		'tr': 'Aynı anda sadece beş tarikat üyesine sahip olabilirsin! Başka bir oyuncuyu öldürmek için birini kurban edebilir veya uykuya geri dönebilirsin.'
	},
	'role_sect_leader_maximum_members': {
		'en': 'You can only have five sect members at once. There is nothing left for you to do this night',
		'ru': 'В твоей секте может быть только пять членов одновременно. Этой ночью делать больше нечего',
		'tr': 'Aynı anda sadece 5 tarikat üyen olabilir. Bu gece yapacak bir şey kalmadı'
	},
	'role_sect_leader_sacrifice_killed_member': {
		'en': 'Sect member {0} has been sacrificed in a dark ritual by their sect leader.',
		'ru': 'Член секты {0} был принесен в жертву в темном ритуале их лидером секты.',
		'tr': 'Tarikat üyesi {0} karanlık bir ayine tarikat lideri tarafından kurban edildi.'
	},
	'role_sect_member_fled': {
		'en': 'Sect member {0} fled the village.',
		'ru': 'Член секты {0} сбежал из деревни.',
		'tr': 'Tarikat üyesi {0} köyden kaçtı.'
	},
	'role_seer_apprentice_became_seer': {
		'en': 'A seer has died. You have become the new seer!',
		'ru': 'Провидец умер. Теперь ты новый провидец!',
		'tr': 'Gözcü öldü. Yeni gözcü artık sensin!'
	},
	'role_seer_apprentice_converted': {
		'en': 'A {0} has died. You have become the new {0}!',
		'ru': '{0} погиб. Теперь ты - новый {0}!',
		'tr': "Bir {0} öldü. Artık yeni {0}'sın!"
	},
	'role_seer_apprentice_reverted': {
		'en': 'A {0} has been revived. You are now a seer apprentice again!',
		'ru': '{0} был воскрешён. Ты теперь снова ученик провидца!',
		'tr': 'Bir {0} canlandırıldı. Artık yeniden bir gözcü çırağısın!'
	},
	'role_shapeshifter_you_shapeshifted': {
		'en': 'You killed {0} and shapeshifted into their role.',
		'ru': 'Ты убил {0} и вжился в его роль.',
		'tr': "{0}'ı öldürdün ve onun kılığına girdin."
	},
	'role_sheriff_no_result': {
		'en': 'You could not get any information last night.',
		'ru': 'Тебе не удалось получить информацию прошлой ночью.',
		'tr': 'Geçen gece hiçbir bilgi alamadın.'
	},
	'role_sheriff_sus_players': {
		'en': 'Your target was either killed by {0} or by {1}.',
		'ru': 'Твоя цель была убита {0} или {1}.',
		'tr': 'Seçtiğin kişi, {0} ya da {1} tarafından öldürülmüş olabilir.'
	},
	'role_sheriff_sus_players_multi': {
		'en': 'Your targets {0} and {1} were killed by {2} or {3}.',
		'ru': 'Твои цели {0} и {1} были убиты {2} или {3}.',
		'tr': 'Hedeflerin {0} ve {1}, {2} veya {3} tarafından öldürüldü.'
	},
	'role_sheriff_sus_players_single': {
		'en': 'Your target {0} was either killed by {1} or {2}.',
		'ru': 'Твоя цель {0} была либо убита {1}, либо {2}.',
		'tr': 'Hedefin {0} ya {1} ya da {2} tarafından öldürüldü.'
	},
	'role_siren_attack_failed': {
		'en': 'You could not entrance {0} last night.',
		'ru': 'Ты не смог ввести {0} в транс прошлой ночью.',
		'tr': "Dün gece {0}'ı büyüleyemedin."
	},
	'role_siren_kill_drown': {
		'en': 'The siren has drowned and killed {0}.',
		'ru': 'Сирена утопила и убила {0}.',
		'tr': "Deniz kızı {0}'ı boğarak öldürdü."
	},
	'role_siren_kill_suicide': {
		'en': '{0} was entranced by a siren that was killed and has fled the village.',
		'ru': '{0} был введён в транс умершей сиреной и сбежал из деревни.',
		'tr': '{0}, deniz kızı tarafından büyülenmişti ve deniz kızı öldüğünde köyden kaçtı.'
	},
	'role_snatcher_wolf_has_protection': {
		'en': 'You have stolen protection and are shielded from one attack.',
		'ru': 'Ты украл защиту и теперь можешь пережить одну атаку.',
		'tr': 'Koruma çaldın ve bir saldırıdan korunacaksın.'
	},
	'role_snatcher_wolf_no_protection': {
		'en': 'Your target had no protection to steal.',
		'ru': 'У твоей цели не было защиты, которую можно украсть.',
		'tr': 'Hedefinde çalınacak bir koruma yoktu.'
	},
	'role_snatcher_wolf_steal_success': {
		'en': 'You successfully stole protection from your target!',
		'ru': 'Ты успешно украл защиту у своей цели!',
		'tr': 'Başarıyla hedefinden koruma çaldın!'
	},
	'role_sorcerer_converted': {
		'en': 'There are no werewolves left. {0} has been converted to a {1}!',
		'ru': 'Все оборотни умерли. {0} был обращён в {1}!',
		'tr': "Kurt adam kalmadı. {0} bir {1} 'e dönüştürüldü!"
	},
	'role_sorcerer_disguised': {
		'en': 'You have disguised yourself as a {0}!',
		'ru': 'Ты замаскировался под {0}!',
		'tr': 'Kendini bir {0} olarak gizledin!'
	},
	'role_sorcerer_resign': {
		'en': 'If you resign you will turn into regular werewolf!',
		'ru': 'Если ты откажешься от своей роли, то превратишься в обычного оборотня!',
		'tr': 'Eğer ayrılırsan normal bir kurt adama döneceksin!'
	},
	'role_soulbinder_bound': {
		'en': 'You have bound yourself to {0}. You can now chat with them privately.',
		'ru': 'Ты связал себя с {0}. Теперь ты можешь общаться с ним приватно.',
		'tr': "Kendini {0}'a bağladın. Artık onunla özel olarak konuşabilirsin."
	},
	'role_soulbinder_bound_to': {
		'en': 'The Soulbinder {0} has bound themselves to you. You can now chat with them privately.',
		'ru': 'Портной душ {0} связал тебя с собой. Теперь ты можешь общаться с ним приватно.',
		'tr': 'Ruh bağlayan {0} kendini sana bağladı. Artık onunla özel olarak konuşabilirsin.'
	},
	'role_spirit_seer_no_killer': {
		'en': 'Your targets did not kill last night.',
		'ru': 'Твои цели не убивали прошлой ночью.',
		'tr': 'Dün gece hedeflerin kimseyi öldürmedi.'
	},
	'role_spirit_seer_sus': {
		'en': 'One of your targets has killed someone last night.',
		'ru': 'Одна из твоих целей убила кого-то прошлой ночью.',
		'tr': 'Hedeflerinden biri gece birini öldürdü.'
	},
	'role_spirit_seer_sus_used': {
		'en': 'You chose to watch this player. When the next day starts you will see if one of your selected players has killed someone this night.',
		'ru': 'Ты решил наблюдать за этими игроками. Когда начнется следующий день, ты увидишь, убил ли один из выбранных тобой игроков кого-то этой ночью.',
		'tr': 'Bu kişiyi izlemeye karar verdin. Yeni bir gün başladığında seçtiğin kişinin önceki gece birini öldürüp öldürmediğini göreceksin.'
	},
	'role_split_wolf_last_night_warning': {
		'en': 'You have not bound yourself to anyone yet. Tonight is your last chance!',
		'ru': 'Ты себя ещё ни с кем не связал. Сегодня твоя последняя возможность сделать это!',
		'tr': 'Kendini henüz kimseye bağlamadın. Bu gece son şansın!'
	},
	'role_split_wolf_split_canceled': {
		'en': 'Your target died before you managed to finish your binding. You should be more careful!',
		'ru': 'Твоя цель умерла раньше, чем ты привязался к ней. Тебе следует быть осторожней!',
		'tr': 'Sen bağlamayı bitiremeden hedefin öldü. Daha dikkatli olmalısın!'
	},
	'role_split_wolf_split_notification': {
		'en': 'The {0} has bound to {1}.',
		'ru': '{0} привязался к {1}.',
		'tr': "{0}, {1}'e bağlandı."
	},
	'role_swamp_wolf_flood_activated': {
		'en': '{0} has activated their flood ability! The chat will be limited during the next day.',
		'ru': '{0} использовал свою способность и затопил деревню! Теперь сообщения в нем будут ограничены в течение следующего дня.',
		'tr': '{0} sel yeteneğini etkinleştirdi! Sohbet önümüzdeki gün boyunca sınırlı olacaktır.'
	},
	'role_swamp_wolf_flood_activated_village': {
		'en': 'A swamp wolf has cast a spell last night. The village is flooded. Everyone will only be able to send a single three letter message this day!',
		'ru': 'Болотный оборотень использовал свое заклинание прошлой ночью. Теперь деревня затоплена. Каждый сможет отправить всего лишь одно трехбуквенное сообщение в чат этим днем!',
		'tr': 'Bir batık kurt dün gece büyü yaptı. Köy sular altında kaldı. Bugün herkes sadece üç harfli tek bir mesaj gönderebilecek!'
	},
	'role_swamp_wolf_your_vote_faked': {
		'en': 'Your vote is being faked by a swamp wolf! Everyone sees you as voting for {0}.',
		'ru': 'Твой голос был фальсифицирован болотным оборотнем! Все видят, что ты голосуешь за  {0}.',
		'tr': "Oyunuz bir batık kurt tarafından taklit ediliyor! Herkes seni {0}'a oy vermiş olarak görüyor."
	},
	'role_tough_guy_die': {
		'en': 'You have been wounded and will die at the end of the day.',
		'ru': 'Ты был ранен и умрёшь в конце дня.',
		'tr': 'Yaralandın ve günün sonunda öleceksin.'
	},
	'role_tough_guy_self_attacked': {
		'en': 'You have been attacked by {0}.',
		'ru': 'Тебя атаковал {0}.',
		'tr': '{0} sana saldırdı.'
	},
	'role_tough_guy_was_attacked': {
		'en': '{0} is a tough guy! They now know your role!',
		'ru': '{0} оказался силачем! Теперь ему известна твоя роль!',
		'tr': '{0} sert adam! Artık senin rolünü biliyor!'
	},
	'role_toxic_wolf_chat': {
		'en': 'The toxic wolf poisoned {0}.',
		'ru': 'Токсичный оборотень отравил {0}.',
		'tr': "Zehirli kurt {0}'ı zehirledi."
	},
	'role_toxic_wolf_chat_poison_removed': {
		'en': 'The poison has been removed from {0}. Attacks against them will no longer ignore protections.',
		'ru': 'Яд был убран с {0}. Атаки против него больше не игнорируют защиту.',
		'tr': '{0} oyuncusundan zehir kalktı. Bu oyuncu artık kurt adam saldırılarına karşı korunabilecek.'
	},
	'role_trapper_trap_killed': {
		'en': "The trapper's trap killed {0}.",
		'ru': 'Ловушка егеря убила {0}.',
		'tr': "Tuzakçının tuzağı {0}'ı öldürdü."
	},
	'role_warden_gave_weapon': {
		'en': 'You gave a weapon to {0} and {1}.',
		'ru': 'Ты отдал оружие {0} и {1}.',
		'tr': "{0} ve {1}'e bir silah verdin."
	},
	'role_warden_jailed_you': {
		'en': 'You are in jail together with {0}. You can chat with them here. But be careful, the warden can hear everything you say.',
		'ru': 'Ты в карцере вместе с {0}. Ты можешь поговорить с ним. Но учти, что надзиратель где-то рядом подслушивает вас.',
		'tr': '{0} ile birlikte hapishanedesin. Onunla burada konuşabilirsin. Ama dikkat et, koğuş bekçisi her dediğini duyabilir.'
	},
	'role_warden_kill_msg': {
		'en': 'The warden gave you a weapon. You can use it to kill the other jailed player. If you try to kill a villager, the weapon will backfire and kill you instead.',
		'ru': 'Надзиратель дал тебе оружие. Ты можешь использовать его, чтобы застрелить своего сокамерника. Однако, если ты попытаешься убить жителя, то пуля отрикошетит в тебя.',
		'tr': 'Koğuş bekçisi sana bir silah verdi. Bunu hapisteki diğer oyuncuyu öldürmek için kullanabilirsin. Bir köylüyü öldürmeye çalışırsan silah geri tepecek ve seni öldürecek.'
	},
	'role_warden_weapon': {
		'en': 'The warden has dropped a weapon into your cell. If you want, you can use it to kill {0}.',
		'ru': 'Надзиратель подкинул оружие в вашу камеру. Если хочешь, ты можешь застрелить {0}.',
		'tr': "Koğuş bekçisi hücrene bir silah attı. İstersen bunu {0}'ı öldürmek için kullanabilirsin."
	},
	'role_was_revealed': {
		'en': "A pacifist has revealed this player's role to everyone!",
		'ru': 'Пацифист раскрыл роль этого игрока всем!',
		'tr': 'Bir barışsever bu oyuncunun rolünü herkese açıkladı!'
	},
	'role_watchdog_your_guard_dog_protected_from_solo_killer': {
		'en': 'Your guard dog protected {0} from a solo killer last night!',
		'ru': 'Твоя сторожевая собака спасла {0} от одиночного убийцы прошлой ночью!',
		'tr': "Bekçi köpeğin dün gece {0}'ı solo katillerden korudu!"
	},
	'role_watchdog_your_guard_dog_protected_from_ww': {
		'en': 'Your guard dog protected {0} from werewolves last night!',
		'ru': 'Твоя сторожевая собака спасла {0} от оборотней прошлой ночью!',
		'tr': "Bekçi köpeğin dün gece {0}'ı kurt adamlardan korudu!"
	},
	'role_werewolf_fan_converted_ww': {
		'en': '{0} was werewolf fan and has been converted into a werewolf!',
		'ru': '{0} был фанатом оборотней и был превращен в оборотня!',
		'tr': '{0} kurt adam hayranıydı ve şimdi kurt adam oldu!'
	},
	'role_werewolf_fan_revealed': {
		'en': 'The werewolf fan {0} has revealed their role to you.',
		'ru': 'Фанат оборотней {0} раскрыл тебе свою роль.',
		'tr': 'Kurt adam hayranı {0} rolünü sana açıkladı.'
	},
	'role_werewolf_fan_revealed_wolves': {
		'en': 'The werewolf fan {0} has revealed their role to the werewolves.',
		'ru': 'Фанат оборотней {0} раскрыл свою роль оборотням.',
		'tr': 'Kurt adam hayranı {0} rolünü kurt adamlara açıkladı.'
	},
	'role_witch_killed': {
		'en': 'The witch killed {0}.',
		'ru': 'Ведьма убила {0}.',
		'tr': "Cadı {0}'ı öldürdü."
	},
	'role_witch_protection_used': {
		'en': 'Last night your potion saved the life of {0}!',
		'ru': 'Прошлой ночью твоё зелье спасло жизнь {0}!',
		'tr': "Dün gece iksirin {0}'ın hayatını kurtardı!"
	},
	'role_wolf_summoner_revived_player': {
		'en': 'The wolf summoner revived {0}.',
		'ru': '{0} был воскрешен волчьим призывателем.',
		'tr': "Sihirdar kurt {0}'ı canlandırdı."
	},
	'role_wolf_summoner_time_over': {
		'en': "{0}'s time is over and they went back to their grave.",
		'ru': 'Время {0} подошло к концу, и он вернулся в могилу.',
		'tr': "{0}'ın zamanı doldu ve mezarına geri döndü."
	},
	'role_wolf_summoner_you_revived': {
		'en': 'You have been revived by the wolf summoner. You will continue playing as regular werewolf until the beginning of the next voting phase.',
		'ru': 'Ты был воскрешен волчьим призывателем. Ты продолжишь играть за обычного оборотня до начала следующего этапа голосования.',
		'tr': 'Sihirdar kurt tarafından canlandırıldın. Bir sonraki oylama aşamasının başlangıcına kadar normal kurt adam olarak oynayacaksın.'
	},
	'role_wolf_summoner_you_revived_perm_revive': {
		'en': 'You have been revived by the wolf summoner. You will continue playing as regular werewolf.',
		'ru': 'Ты был возрожден волчьим призывателем. Ты продолжишь играть за обычного оборотня.',
		'tr': 'Sihirdar kurt tarafından canlandırıldın. Sıradan kurt adam olarak oynamaya devam edeceksin.'
	},
	'role_yule_wolf_system_kill': {
		'en': '{0} has sacrificed themself to the yule wolf to free the other players trapped with them.',
		'ru': '{0} пожертвовал собой ради Йольского оборотня, чтобы освободить других игроков, оказавшихся с ним в ловушке.',
		'tr': '{0} diğer tutsakları özgür bırakmak için kendisini zemheri kurta feda etti.'
	},
	'role_yule_wolf_system_sacrifice_protected': {
		'en': 'You sacrificed yourself but survived. You are no longer role blocked.',
		'ru': 'Ты принёс себя в жертву, но при этом выжил. Твоя роль больше не заблокирована.',
		'tr': 'Kendini feda ettin ama hayatta kaldın. Artık rolün engellenmeyecek.'
	},
	'role_yule_wolf_system_selection_failed': {
		'en': 'One or more of the players you chose died before the phase began, so the ability did not activate.',
		'ru': 'Один или несколько выбранных игроков умерли до начала фазы, поэтому способность не активировалась.',
		'tr': 'Seçtiğin oyuncuların en az biri sonraki aşamadan önce öldü, bu yüzden yeteneğin aktif olmadı.'
	},
	'role_yule_wolf_system_selection_success': {
		'en': 'You have successfully selected {0}, {1} and {2}. They are now role‑blocked until either one of them sacrifices themselves or you are killed.',
		'ru': 'Ты успешно выбрал игроков {0}, {1} и {2}. Теперь их роли заблокированы, пока один из них не принесёт себя в жертву или пока ты не погибнешь.',
		'tr': 'Başarıyla {0}, {1} ve {2} oyuncularını seçtin. Sen ölene veya birisi kendini feda edene kadar yeteneklerini kullanamayacaklar.'
	},
	'role_yule_wolf_system_self_selected': {
		'en': 'You, {0} and {1} have drawn the yule wolf’s ire. All three are role‑blocked.',
		'ru': 'Ты, {0} и {1} разгневали Йольского оборотня. Все трое заблокированы по роли.',
		'tr': "Sen, {0} ve {1} Zemheri Kurt'un sinirine geldiniz. Üçünüz de yeteneklerinizi kullanamazsınız."
	},
	'role_yule_wolf_system_unblocked': {
		'en': 'The yule wolf has been killed and you are no longer role blocked.',
		'ru': 'Йольский оборотень умер, и ты больше не заблокирован по роли.',
		'tr': 'Zemheri kurt öldü ve artık yeteneklerini kullanabilirsin.'
	},
	'role_yule_wolf_system_unblocked_sacrifice': {
		'en': '{0} sacrificed themselves to divert the yule wolf’s attention. You are no longer role‑blocked.',
		'ru': 'Игрок {0} принёс себя в жертву, чтобы отвлечь внимание Йольского оборотня. Твоя роль больше не заблокирована.',
		'tr': "{0} Zemheri Kurt'un dikkatini dağıtmak için kendini feda etti. Artık yeteneklerini kullanabilirsin."
	},
	'role_zombie_killed_decay': {
		'en': 'The body of {0} has decayed and they are now dead!',
		'ru': 'Тело {0} прогнило и теперь он окончательно мертв!',
		'tr': "{0}'ın bedeni çürüdü ve şimdi öldü."
	},
	'role_zombie_killed_werewolf': {
		'en': '{0} tried to bite a werewolf but ended being eaten instead!',
		'ru': '{0} попытался укусить оборотня, но его моментального съели!',
		'tr': '{0} bir kurt adamı ısırmaya çalıştı ama onun yerine kendisi yenildi.'
	},
	'role_zombie_remaining_days': {
		'en': 'You will decay and die in {0} day(s).',
		'ru': 'Ты разложишься и умрешь через {0} дней.',
		'tr': '{0} gün içinde çürüyüp öleceksin.'
	},
	'weather_thunderstorm_killed_player': {
		'en': '{0} got struck by lightning and died.',
		'ru': '{0} погиб от удара молнии.',
		'tr': "{0}'ın üzerine yıldırım düştü ve öldü."
	},
	'werewolf_chat_blind_werewolf_resigned': {
		'en': '{0} resigned as blind werewolf.',
		'ru': '{0} отказался от своих способностей.',
		'tr': '{0} kör kurt adam olmaktan ayrıldı.'
	},
	'werewolf_chat_blind_werewolf_view': {
		'en': 'The blind werewolf checked {0}',
		'ru': 'Слепой оборотень проверил {0}',
		'tr': "Kör kurt adam, {0}'ı kontrol etti"
	},
	'werewolf_chat_blind_werewolf_view_aura': {
		'en': 'The blind werewolf sensed the aura of {0}',
		'ru': 'Слепой оборотень учуял ауру {0}',
		'tr': "Kör kurt adam {0}'ın aurasını hissetti"
	},
	'werewolf_chat_nightmare_werewolf_used_asleep': {
		'en': 'The nightmare werewolf put {0} to sleep.',
		'ru': 'Кошмарный оборотень усыпил {0}.',
		'tr': "Kabus kurt adam {0}'ı uyuttu."
	},
	'werewolf_chat_sorcerer_resigned': {
		'en': '{0} resigned as sorcerer and is now a {1}.',
		'ru': '{0} отказался от роли волшебника и теперь {1}.',
		'tr': '{0} büyücü olmaktan ayrıldı ve şu an {1}.'
	},
	'werewolf_chat_voodoo_werewolf_used_asleep': {
		'en': 'The voodoo werewolf put {0} to sleep.',
		'ru': 'Вуду-оборотень усыпил {0}.',
		'tr': "Vudu kurt adam, {0}'ı uyuttu."
	},
	'werewolf_chat_wolf_seer_resigned': {
		'en': '{0} resigned as wolf seer.',
		'ru': '{0} отказался от способностей провидца.',
		'tr': '{0} kurt gözcüsü olmaktan ayrıldı.'
	},
	'werewolf_chat_wolf_seer_view_role': {
		'en': 'The wolf seer checked {0}.',
		'ru': 'Волчий провидец проверил {0}.',
		'tr': "Kurt gözcü {0}'ı kontrol etti."
	},
	'werewolf_chat_wolf_seer_view_role_can_convert': {
		'en': 'Biting this player will convert them into a regular werewolf!',
		'ru': 'Укусив этого игрока, вы превратите его в обычного оборотня!',
		'tr': 'Bu oyuncuyu ısırmak onu normal kurt adama dönüştürecektir!'
	},
	'werewolf_chat_wolf_seer_view_role_cannot_kill': {
		'en': 'As a werewolf you cannot kill this role during the night!',
		'ru': 'Будучи оборотнем, ты не можешь убить эту роль ночью!',
		'tr': 'Kurt adam olarak bu rolü gece öldüremezsin!'
	},
	'werewolf_chat_wolf_shaman_enchanted': {
		'en': 'The wolf shaman enchanted {0}.',
		'ru': 'Волчий шаман зачаровал {0}.',
		'tr': 'Şaman kurt {0}’ı kutsadı.'
	},
	'wolf_magician_chat_revoked': {
		'en': 'Your transformation ability has been revoked.',
		'ru': 'Твоя способность превращаться была утрачена.',
		'tr': 'Dönüşme yeteneğin geri çekildi.'
	},
	'wolf_magician_chat_selected': {
		'en': 'A wolf magician wants to convert you to {0}.',
		'ru': 'Магический волк хочет превратить тебя в {0}.',
		'tr': 'Bir sihirbaz kurt seni {0} rolüne dönüştürmek istiyor.'
	},
	'wolf_magician_chat_transformed': {
		'en': '{0} has transformed into {1}.',
		'ru': '{0} трансформировался в {1}.',
		'tr': '{0}, {1} rolüne dönüştü.'
	},
	'wolf_magician_chat_transformed_private': {
		'en': 'You have been converted to {0} by the wolf magician.',
		'ru': 'Ты был превращён в {0} магическим волком.',
		'tr': 'Sihirbaz kurt tarafından {0} rolüne dönüştürüldün.'
	},
}

DISCUSSION_PREFIXES = (
	'Discussion',
	'Обсуждение',
	'Tartışma'
)

VOTING_PREFIXES = (
	'Voting',
	'Голосование',
	'Oylama'
)

UI = {
	'werewolf_chat': ('Werewolf chat',        'Чат оборотней',            'Kurt adam sohbeti'),
	'join':          ('Join',                 'Присоединиться',           'Katıl'),
	'cancel':        ('Cancel',               'Отмена',                   'Vazgeç'),
	'ok':            ('OK',                   'Окей',                     'Tamam'),
	'continue':      ('Continue',             'Продолжить',               'Devam et'),
	'play_again':    ('Play again',           'Играть снова',             'Tekrar oyna'),
	'refresh':       ('Refresh',              'Обновить',                 'Yenile'),
	'custom_games':  ('Custom games',         'Персонализированные игры', 'Özel oyunlar'),
	'quick_game':    ('Quick game',           'Быстрая игра',             'Hızlı oyun'),
	'create_game':   ('Create game',          'Создать игру',             'Oyun oluştur'),
	'start_game':    ('Start game',           'Начать игру',              'Oyunu başlat'),
	'play':          ('Play',                 'Играть',                   'Oyna')
}

_PLAYER_RE = r'\d{1,2} \S+(?:\s+\([^)]+\))?'
_WORD_RE = r'\S+'

_PATTERNS = None
_WINNER_KEYS = frozenset(k for k in _STRINGS if k.startswith('chat_message_winner_'))
_UI_LOOKUP = {v.upper(): key for key, variants in UI.items() for v in variants}


def _template_to_regex(template, word_slots=None):
	word_slots = word_slots or set()
	placeholders = re.findall(r'\{(\d+)\}', template)
	parts = re.split(r'\{\d+\}', template)

	seen_indices = set()
	pattern_parts = []

	for i, literal in enumerate(parts):
		escaped = re.escape(literal.strip())

		if escaped:
			pattern_parts.append(escaped)

		if i < len(placeholders):
			n = placeholders[i]
			n_int = int(n)

			if n not in seen_indices:
				rx = _WORD_RE if n_int in word_slots else _PLAYER_RE
				pattern_parts.append(f'(?P<p{n}>{rx})')
				seen_indices.add(n)

			else:
				rx = _WORD_RE if n_int in word_slots else _PLAYER_RE
				pattern_parts.append(f'(?:{rx})')

	full = r'\s*'.join(filter(None, pattern_parts))

	return re.compile(full, re.IGNORECASE | re.DOTALL)

def _build_patterns():
	seen = set()
	result = []

	for key, translations in _STRINGS.items():
		word_slots = translations.get('_word_slots', set())

		for lang, template in translations.items():
			if lang.startswith('_'):
				continue

			template = template.strip()

			if template in seen:
				continue

			seen.add(template)

			try:
				result.append((key, _template_to_regex(template, word_slots)))
			except re.error:
				pass

	return result

def match_event(message):
	msg = message.strip()

	for key, pattern in _PATTERNS:
		m = pattern.fullmatch(msg)

		if m is None:
			m = pattern.search(msg)

		if m:
			result = {'event': key}

			for name, value in m.groupdict().items():
				if value is not None:
					result[name] = value.strip()

			return result

def is_winner_event(event_key):
	return event_key in _WINNER_KEYS

def is_game_phase(text):
	return text.endswith('s') or text.startswith(VOTING_PREFIXES + DISCUSSION_PREFIXES)

def is_voting_phase(text):
	return text.startswith(VOTING_PREFIXES)

def is_discussion_phase(text):
	return text.startswith(DISCUSSION_PREFIXES)

def is_ui(text, key):
	return text.upper() in {v.upper() for v in UI[key]}

def match_ui(text):
	return _UI_LOOKUP.get(text.upper())

def ui_re(key):
	pattern = '|'.join(re.escape(v) for v in UI[key])

	return re.compile(pattern, re.IGNORECASE)

def parse_player_token(token):
	token = re.sub(r'\s*\([^)]*\)', '', token).strip()
	parts = token.split(' ', 1)

	return int(parts[0]) - 1, parts[1]

def extract_role_from_token(token):
	m = re.search(r'\(([^)]+)\)', token)

	if not m:
		return

	content = m.group(1)

	if '/' in content:
		return content.split('/')[-1].strip()

	return content.strip()


_PATTERNS = _build_patterns()
