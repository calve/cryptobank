import unittest
import string
from cryptobank.monrsa.crypto import generate_keys, Key, _is_prime, _get_prime
from cryptobank.test.unittests import randomword

pubkey_1 = b'eyJtb2R1bHVzIjogMjAxNDc3OTI5MzI0MDY4MDQ2MzQ3MzE1MzYwMzQxMTUxNTA1Mjc0MTgyOTI0NDEwMDE5Mjc1Mzc4MjUxNDgxNzg1MjgwMDY0OTg0NTQyMTY4NzEzODkwOTE3ODg3NTg4MDg0MzI1OTg2NTU3MjAyMTgxNTUwOTIwMjUxMzYyMTU5OTI0Njg4MjY1OTg4NDQzMjIxOTM4NTQxNTY5MzcyOTE4MTcxMjIzMDQ2MTM2MjY1OTkzMDQ2MjAwNzQxMTYzMjEzNzM5NzI2MTk5NzI1NDEyMjI1MjEzNDk2MjUxMDYwNTY3NzI5MTU0MzIwNDc5ODI0NTAzMzA2MjEyNTgxMjQwMTMxMjEwNjM3MTgwOTUzNjg3NTE1ODI5MDg4OTc2NTcxNDI1MDA1ODI1Njg5MjQwNDQwNDIzNTYzMzA0NTIwMDg1OTQwOTYzMzc4MTA4NzEyNjY3NjExMTM5MDAyMDkxMjY0OTQ5MTYzMTIwODUwNDQ1OTUzNjc5NTM0MjU0MTUzNzMzODA1OTk3NzcyMzkzNzA0MjMwNjM0NDAyOTUzOTE2Njk3NjgyNTUyNTgzNzQwNDU2MzUxMDQwMDk3MDQwNjA5NTE0MDE2NzM0MTAzMTc3MzU4MTUwNTk5OTEwODkzMzYzOTA0OTg2MTY5Nzk3NTQ4MzY4MDkwMzAyNjU1MzE4NzEwMjEwMTg2OTU2MjM4ODM4MTcwNDY0ODIxODM1OTY0NTY5OTQ2MzE1MjQ5MDY0NDk0MjM2NDUzMzcwNjEwMjc5MjU0MDY0NDU3MDU1OTM3ODcxMzYwNTE5Nzg5MzEzNTg4MjcsICJlbmNyeXB0aW9uIGV4cG9uZW50IjogMTg4OTczMjY4ODQyMDI2NDEyMzQzODE3MjQyMTc0ODg5NTg5OTUxOTA3OTcxMjIwMDMyMzM1NDI2ODQzMTY5NTI4NzQ0ODg4MTA4Njk1NzM3MzA5NDQ2MjI4MzUzNTQzOTcyNDQzMTc4NTk2NDk5MTU1MjgzODU1MTczNzMzMTA0MDIzMTQ3NDA5MTQ1NzAyNjU0NzQ1MjMyNzIwOTkxMzE3MTQ4OTY3NTYwNTIyNjk0OTA5NjIyMzA1MDMyMjU3MjIxMzIyMTExMTU5MDU3NDI0MDM5OTY5ODA3MTExMTk4NTAyNDgzNTU2ODAyMTkxNDg1MzYzOTU2ODc1NzE0Mjk3MjI4NzUyMzQyMTg1NDI2NjAyNzI0MTMwNzIwOTA5Nzk1Njc1MDIwNDI5MTQxMjI2ODk4NTA2NDIzMzQyNzc1MjQxNTI5NTUwNTEwNzU0NDcwMTY5NzE5OTY0NTc1ODc3ODUxMDgyNzk2NDkxNjY4MDEwNTU4ODg0NjQ1MDU4Nzc1MjkyMzYyODAxOTc0MzI1NDQ0OTYxMDQ1MTk0MDM1NTczOTc0NTg5ODA3MDc4NTEzNDEzMDQzODAyNDU0MDgxNzg5ODAwMDA4ODM5NTE5NjM5MDIzNjYwODk4NzM2NTM2OTYyMjQ2NzcwNzEzNjkxNjIzMDcwNTY2NzY4NjEyMDg4NzE2MjI3OTQwMjA5MTQwOTE0Mzk1Njc1OTY2OTg3ODg3Mzk0MjE1Nzk2MDQ2MTA1NDQxMDY4NjUzMzU5NTgzMjQyNDY0ODUyMzQxMDE3OTkwMTgzMTY5MDY2OTI1NzM0MDkzMTV9'
privatekey_1 = b'eyJtb2R1bHVzIjogMjUyMjQ3MjA2NzQ1MjA1MTY3NjQwMjY5NzgyMzczNDI5MzYwNTAyNzg1Njc1MjIzNDc2Njk2NTkwNTI0MjI5Nzk1NDQ0NDUyMzEyMzY2MDM4NzcyMDczMTY5MDY3MDcwMzc2MTIwMjgxMjI0MTAxNzE3MTg0NzIzMDA4NTk3MzQ1OTQ2Mjc2ODA5ODQxMzY2NTAzNzIzNTE0NDQwMzEwMDc4NjE0NzY3OTkyMzY0MTc0OTkwNTM0MjAwMDA0ODEyMjQyMTk4NTEyMTExNzc5ODMwMjAyMjA4MjMxMTk0NzUwODE5MDUxMTg0Nzk5MTkyMjI1OTIxNjQyNDI5MzIwNDQ0NjY4NzY0MTcxNzU4NDkwOTAzODM3MDQ1NDk3MzI3NDI3MDE0ODIxNDAwMDc3NjM5MTU1OTA2NzY1MTI0MDk3MTY5NjU2MjE5NjU1MTM1MzYwMzk1NDQ1OTQ0Mjg0MzY4MzM2Mzk4NTc2OTM4NTIzMDg1MzE1OTg1Mjg2NzI1ODQ3MzMzMjA4MDIwODU4MDY2Njg3MTUwMjc3NDI3ODYwOTMyMDQ3ODI5MDQyNDE4NzM3NzE3NzAzNzkzNjExOTU4Mjg0NzUwOTk2MzQ4OTM2NDM5MDE2MzAzODA0OTg1NjQxMDU0MTk3MTk0NzU1OTQ2NzY1MTYzNDIzMzE3MzM2MjA5NTc5MTIzOTM5NTUzNDY2Mjc3MzExMDYyMjc1ODQwOTUyMjc4OTg5NDg2NzAzNjMwMTA0NjE5NzA5MzAwMDgwMzM5MjY4MzU1NTU0Mzg4NDQ2MDc5MzgwMjEzNzkyMDkwNjU1MzMsICJlbmNyeXB0aW9uIGV4cG9uZW50IjogMTYxMTE5NzIzNDIzNDIwMzA4NDU4MDc5MjAzOTAzOTk1NTE0NjYwMzI3OTk4OTE1NDYwMzc0MjcxNjg2NjU2MTYyMzYzNjkyNTQ4NzAwNzk3Nzc2OTg2MzIxNjc3MTg4NTMzNDg1NDUyNTk2NDk2MTM1MjE0MTg3NzQ5NDkxNTEzMTg5MzE2NjIyNjcxMjA2NDU4NjA3NTc1NjA5MDg3NDA0NzU1NDk4NzkzMTAxMTU2MTUwNTExNzExMDQ0MDc4NTQ2ODAwOTc4NTg4MDAwNTg2OTE5MDcxMTQ4NTc2MDUxODg5NjczMzI0NTIxMjU2MDEyNzM2NjU4NzcyODA5NzU5NTA2NzYyMTgxMjk0NTMwMjM5MzczNDIwMjgxMTc2Mzk3NzM2MzA2MDU3MzkxNTEzNDUzOTc4OTg0MzkxOTI0MTMwOTk0MjQ0NjgwODY1Njc4MzY3NjA3MTQ0MzM2MTExMTMzOTg3ODQyNTY5ODY2MDgzNTU2OTI2OTYzMTU5NjQxNTY1OTUzODE5MjI0NTQzNjM5MDE2MDc1MjY4NzcyNzAwNDQwMDE0NDM2MzQ0OTgwODI0MTY4NjAzMDE5NjA3MzA0NDAzOTQzNzY2MzcyNTY4Mzk0NTA5NjI3MjIxNTIwOTA1MjY0NTA4OTEzMzI3NDYzMDEyOTIyNTg0NzcxNjU0NjE5MjUzNDg3NzI3MDQ4OTU1Njk1NzA3ODU0NzM2ODUxMDkxMTE3ODY2ODQwNzYzNjg2NzI4MjQ2OTA4MjQyMTk1NDE3ODEwNzUwNjAzOTIzNDA0MTQ5MjQ2ODM3OTgxMTQzNTEsICJkZWNyeXB0aW9uIGV4cG9uZW50IjogMTQxMDk2NzIzMDc5OTE3NzQxNzA0MjM4NTQxMjQxMjAwMjI2MTQyNzM0ODY5NDMzNjIwODcyNzI1MDUxNTkxMTA5NTE3NzMyMzYyMzQ4MzE1MTc2MjE2NjkzOTgwOTgyMDk5MDIwNTIzNzAyMjA2NjA5NDk0Mjk0MTQwMDI4Nzg5ODY0NTc4MzM4NjU5MTkwMTUyOTYwOTU2NjAxMTgwMTY5NDI0NjcyMjc5Mjc1MDY5NTk2MDExODM4NTg1Mjg3MDMxODUwMjc3MzA5MjU3NjcyMDIzMDk0Mzg4NjMwMzAwMDc0OTM4NDQ4OTEyNjIyNDA3NTU1MzE2MzE3NTIxNDA4OTU5NTUwNTA0Njc2NzQxMjMxODE1OTYwNTYzNjQ3OTUyMDY5MzM1ODY1OTkyMzI1MTYyNjMyNDkxMzg5NTY5NDQ0Njg1NjQwMDIxODEzNzk2ODM0OTI3MjE2NzUyMjIwNTYzNzA4ODMxMTY4ODA1NTEyOTY1NTQyNTc1MTUzODQzMzkwNDA2Nzg5MTgyMTMxMzU4MjUwNjk3NjcwMzc2OTY3NDQ4MDY0Njk3OTI0MTY3MjQ4NDM1NzMxODQxMTY0MTYzMDcxMzgzOTYyMjIyMDAxNTAyNTI3NjQyNjE5MTM3ODQ5NjMxMTEyNzM0NTk2NTMyMDUxNjczMzUwODY3ODM2MDM0NzAwMzgwNTY3NzA2Mjg5OTA5NTg5ODMzOTA5Mjk4MjE0MDIyMTI5OTQwMDgzMDExNjIxODg4ODM0ODQxMDgwNjQ0NDA0MzY3MTIzOTYwNDExMzk1Mjc4MzY2MDgxMTQ3MX0='


class TestCrypto(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """
        Runned once
        """
        self.keys = Key.import_key(privatekey_1)

    def test_sign_small_string(self):
        """
        Test that we can sign and verify a small string
        """
        key = self.keys
        for i in range(1, 11):
            random_word = randomword(2 ** i)
            signature = key.sign(random_word)
            try:
                self.assertTrue(key.verify(random_word, signature))
            except AssertionError:
                print("Failed to sign string of length {}".format(2 ** i))
                raise

    def test_sign_public_key(self):
        """
        Test the signature of a signed public key
        """
        key = self.keys
        publickey = key.get_pub().decode()
        signature = key.sign(publickey)
        self.assertTrue(key.verify(publickey, signature))

    def test_prime(self):
        for n in [3, 5, 7, 13, 17, 31]:
            self.assertTrue(_is_prime(n))
        for n in [0, 1, 4, 6, 9, 15, 20, 100]:
            self.assertFalse(_is_prime(n))

    def test_prime_gen(self):
        self.assertTrue(_is_prime(_get_prime(1024)))

    def test_signature(self):
        key = self.keys
        random_words = randomword(255)
        signature = key.sign(random_words)
        self.assertTrue(key.verify(random_words, signature))
        self.assertFalse(key.verify(randomword(255), signature))
        self.assertFalse(key.verify(random_words, randomword(255)))

    def test_key_gen(self):
        key1 = self.keys
        key2 = generate_keys()
        self.assertNotEqual(key1.e, key1.d)
        self.assertNotEqual(key1.e, key2.e)
        self.assertNotEqual(key1.d, key2.d)

    def test_import(self):
        k = Key.import_key(pubkey_1)
        self.assertEqual(k.e, 18897326884202641234381724217488958995190797122003233542684316952874488810869573730944622835354397244317859649915528385517373310402314740914570265474523272099131714896756052269490962230503225722132211115905742403996980711119850248355680219148536395687571429722875234218542660272413072090979567502042914122689850642334277524152955051075447016971996457587785108279649166801055888464505877529236280197432544496104519403557397458980707851341304380245408178980000883951963902366089873653696224677071369162307056676861208871622794020914091439567596698788739421579604610544106865335958324246485234101799018316906692573409315)
        k = Key.import_key(privatekey_1)
        self.assertEqual(k.d, 1410967230799177417042385412412002261427348694336208727250515911095177323623483151762166939809820990205237022066094942941400287898645783386591901529609566011801694246722792750695960118385852870318502773092576720230943886303000749384489126224075553163175214089595505046767412318159605636479520693358659923251626324913895694446856400218137968349272167522205637088311688055129655425751538433904067891821313582506976703769674480646979241672484357318411641630713839622220015025276426191378496311127345965320516733508678360347003805677062899095898339092982140221299400830116218888348410806444043671239604113952783660811471)

    def test_file_import(self):
        k = Key.import_key_from_path("./cryptobank/test/example1.privatekey")
        self.assertEqual(k.d, 7260641110672835047827501997505943133111644574566000021223010655821235083273105396166649351538199689087470625243598930260920051965152495026558593677206110131225339468439963696250138457237146400566084663068588989184142313129218072345377097517321866479966875312693812985816283627389031218962071766399892103649986215460566584764250065985145026249061430407197849885219245804705911929101154059227132722588356478832245147574995036068957521408346894233847348879381167232592226850553762509438716835126943861635944585593943577474311423037504121629177079385831326372436253345586993761731264277329967225302363697165149604157685)
