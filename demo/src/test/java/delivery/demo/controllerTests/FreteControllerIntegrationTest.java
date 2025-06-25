package delivery.demo.controllerTests;

import delivery.demo.model.*;
import delivery.demo.service.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class FreteControllerIntegrationTest {
    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate rest;

    @Autowired
    private ClienteService clienteService;

    @Autowired
    private CidadeService cidadeService;

    @Autowired
    private FreteService freteService;

    private Cliente cliente;
    private Cidade cidade;

    private String url(String path) {
        return "http://localhost:" + port + path;
    }

    @BeforeEach
    void setUp() {
        freteService.listarTodos().forEach(f -> freteService.deletar(f.getId()));
        cidadeService.listarTodas().forEach(c -> cidadeService.deletar(c.getId()));
        clienteService.listarTodos().forEach(c -> clienteService.deletar(c.getId()));

        cliente = clienteService.salvar(new Cliente("Marcos", "12323", "Rua ABC"));
        cidade = cidadeService.salvar(new Cidade("São Luís", "MA", 15.0));
    }

    @Test
    @DisplayName("Deve cadastrar o frete com sucesso")
    void deveCadastrarFreteComSucesso() {
        Frete frete = new Frete(cliente, cidade, "Frete 1", 3.0);

        ResponseEntity<Frete> response = rest.postForEntity(url("/fretes"), frete, Frete.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isNotNull();
        assertThat(response.getBody().getValor()).isEqualTo(45);
    }

    @Test
    @DisplayName("Deve buscar fretes por cliente")
    void deveBuscarFretesPorCliente() {
        Frete frete = new Frete(cliente, cidade, "Frete 1", 3.0);
        Frete frete2 = new Frete(cliente, cidade, "Frete 2", 1.0);

        ResponseEntity<Frete[]> response = rest.getForEntity(url("/fretes/cliente/" + cliente.getId()), Frete[].class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).hasSize(2);

    }

    @Test
    @DisplayName("Deve lançar exceção se o cliente não existir")
    void deveLancarExcecaoSeClienteNaoExiste() {
        Cliente falso = new Cliente("Hercules", "888886666", "Olimpo");
        Frete frete = new Frete(falso, cidade, "Entrega dos deuses", 10.0);

        ResponseEntity<String> response = rest.postForEntity(url("/fretes"), frete, String.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.INTERNAL_SERVER_ERROR);
        assertThat(response.getBody()).contains("Cliente não encontrado");
    }

    @Test
    @DisplayName("Deve lançar exceção se a cidade não existir")
    void deveLancarExcecaoSeCidadeNaoExiste() {
        Cidade falso = new Cidade("Terabitia", "TR", 5.0);
        Frete frete = new Frete(cliente, falso, "Entrega dos deuses", 10.0);

        ResponseEntity<String> response = rest.postForEntity(url("/fretes"), frete, String.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.INTERNAL_SERVER_ERROR);
        assertThat(response.getBody()).contains("Cidade não encontrada");
    }
}
