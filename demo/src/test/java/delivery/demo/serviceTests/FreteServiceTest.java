package delivery.demo.serviceTests;

import delivery.demo.model.*;
import delivery.demo.repository.FreteRepository;
import delivery.demo.service.*;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;


import java.util.Optional;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.assertj.core.api.AssertionsForClassTypes.assertThatThrownBy;

@ActiveProfiles("test")
@SpringBootTest
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class FreteServiceTest {

    @Autowired
    private FreteService freteService;

    @Autowired
    private ClienteService clienteService;

    @Autowired
    private CidadeService cidadeService;

    @Autowired
    private FreteRepository freteRepository;

    private Cliente cliente;
    private Cidade cidade;

    @BeforeEach
    void limpar() {
        freteRepository.deleteAll();
        cliente = clienteService.salvar(new Cliente("Carlos", "123123", "Rua ABC"));
        cidade = cidadeService.salvar(new Cidade("São Luís", "MA", 15.0));
    }

    @Test
    @Order(1)
    void deveSalvarComFreteCalculado() {
        Frete frete = new Frete(cliente, cidade, "Entrega 1", 2.0);
        Frete freteSalvo = freteService.salvar(frete);

        double valorEsperado = 2.0 * 10 + 15.0;

        assertThat(freteSalvo.getValor()).isEqualTo(valorEsperado);
    }

    @Test
    @Order(2)
    void deveLancarExcecaoSeClienteNaoExiste() {
        Cliente falso = new Cliente("Impostor", "321321", "Espaço");
        Frete frete = new Frete(falso, cidade, "Entrega 2", 2.0);

        assertThatThrownBy(() -> freteService.salvar(frete))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Cliente não encontrado");
    }

    @Test
    @Order(3)
    void deveLancarExcecaoSeCidadeNaoExiste() {
        Cidade falsa = new Cidade("Nárnia", "NR", 555.0);
        Frete frete = new Frete(cliente, falsa, "Entrega 3", 50.0);

        assertThatThrownBy(() -> freteService.salvar(frete))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Cidade não encontrada");
    }

    @Test
    @Order(4)
    void deveRetornarFreteComMaiorValor() {
        freteService.salvar(new Frete(cliente, cidade, "Frete1", 1.0));
        freteService.salvar(new Frete(cliente, cidade, "Frete2", 2.0));
        freteService.salvar(new Frete(cliente, cidade, "Frete3", 3.0));

        Optional<Frete> maiorFrete = freteService.freteComMaiorValor();

        assertThat(maiorFrete).isPresent();
        assertThat(maiorFrete.get().getDescricao()).isEqualTo("Frete3");
        assertThat(maiorFrete.get().getValor()).isEqualTo(38.0);
    }

    @Test
    @Order(5)
    void deveRetornarCidadeComMaisFretes() {
        Cidade cidade2 = new Cidade("Santo Amaro", "MA", 5.0);
        Frete frete1 = new Frete(cliente, cidade, "Frete 1", 2.5);
        Frete frete2 = new Frete(cliente, cidade, "Frete 2", 3.9);
        Frete frete3 = new Frete(cliente, cidade2, "Frete 3", 1.5);

        Optional<Cidade> maisFretes = freteService.cidadeComMaisFretes();

        assertThat(maisFretes).isPresent();

        assertThat(maisFretes.get().getNome()).isEqualTo("São Luís");
    }
}
